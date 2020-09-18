"""Util functions."""
import logging
import argparse
from functools import reduce
import io
import os
from ast import literal_eval
import json
import re
from tokenize import (untokenize, generate_tokens, ENDMARKER, NEWLINE, INDENT,
                      DEDENT, OP, NAME, NUMBER, STRING, NL, COMMENT)
import requests

from requests.compat import urljoin
import ipykernel
from notebook.notebookapp import list_running_servers
import celltest

root_logger = logging.getLogger()
if not root_logger.handlers:
  logging.basicConfig()

loglevel_old = root_logger.handlers[0].level
logger = logging.getLogger('celltest')
logger.setLevel(loglevel_old)


def _tokenize(string):
  """Make tokens from string."""
  return generate_tokens(io.StringIO(string).readline)


def glue(*args):
  """Glue code."""
  return reduce(glue_pair, args, "")


def glue_pair(code1, code2):
  """Glue two pieces of code."""
  return code1 + code2


def glue_pair_(code1, code2):
  """Glue two pieces of code."""
  # the tokenize method could be preferential if need to align
  # indentation before glueing
  tokens1, tokens2 = _tokenize(code1), _tokenize(code2)
  tokens1 = [(x[0], x[1]) for x in tokens1]
  tokens2 = [(x[0], x[1]) for x in tokens2]
  if tokens1[-1][0] == ENDMARKER:
    del tokens1[-1]
  if tokens1 and tokens1[-1][0] != NEWLINE:
    tokens1 += [(NEWLINE, "\n")]
  tokens = tokens1 + tokens2
  if tokens[-1][0] != ENDMARKER:
    tokens += [(ENDMARKER, "")]

  logger.debug("tokens: %s", tokens)
  return untokenize(tokens)


def indent(code, indentation=4, count=1):
  """Remove indentation at the beginning and end."""
  tokens = [(x[0], x[1]) for x in _tokenize(code)]

  for _ in range(count):
    tokens_ = []
    for token in tokens:
      if token[0] == INDENT:
        token = (INDENT, indentation * " " + token[1])
      tokens_.append(token)
    tokens = tokens_
    if tokens[0][0] != INDENT:
      tokens = [(INDENT, indentation * " ")] + tokens[:-1] + [(DEDENT, "")
                                                             ] + [tokens[-1]]
  logger.debug(tokens)

  tokens = [(NEWLINE, "\n")] + tokens
  result = untokenize(tokens)
  result = "\n".join(result.split("\n")[1:])

  return result


def fully_dedent(code):
  """Remove indentation at the beginning and end."""
  tokens = list(_tokenize(code))
  indent_index = dedent_index = None
  for index, token in enumerate(tokens):
    if token[0] == INDENT:
      indent_index = index
    if token[0] == NEWLINE:
      break

  # this loop is probably redundant
  for index, token in reversed(list(enumerate(tokens))):
    if token[0] == DEDENT:
      dedent_index = index
    if token[0] == NEWLINE:
      break

  tokens_ = [(token[0], token[1]) for token in tokens]
  if indent_index and dedent_index:
    indent_str = tokens[indent_index][1]
    for index, token in enumerate(tokens):
      if token[0] == INDENT:
        tokens_[index] = (token[0], token[1][len(indent_str):])

  logger.debug(tokens_)

  return untokenize(tokens_)


def save_outputs(code):
  """Determine the outputs line.

  It is assumed that outputs line is in the end of the code as
  similar assumption is made by ipython engine
  """
  code = fully_dedent(code)
  tokens = list(_tokenize(code))
  logger.debug("tokenized: %s", tokens)
  last_line_end = None
  last_line_start = 0
  # find last line start and end
  for index, token in reversed(list(enumerate(tokens))):

    if last_line_end is None:
      if token[0] == NEWLINE:
        last_line_end = index
        logger.debug("last_line_end: %d", last_line_end)
        continue
    else:
      if token[0] == NEWLINE:
        last_line_start = index
        logger.debug("last_line_start: %d", last_line_start)
        break
  logger.debug("last line: %s", tokens[last_line_start:last_line_end])

  assigned, expr = None, None
  for index, token in enumerate(tokens[last_line_start:last_line_end]):
    if expr is None:
      if token[0] in [NAME, STRING, NUMBER] or (token[0] == OP and
                                                token[1] in ["{", "["]):
        expr = index + last_line_start
        logger.debug("Name: %s", token[1])
        continue
    else:
      if token[0] == OP and token[1] == '=':
        assigned = index + last_line_start
        break
      if token[0] == OP and token[1] == '(':
        break

  # if var unassigned then assign var
  tokens_ = [(x[0], x[1]) for x in tokens]
  if expr is not None and assigned is None:
    tokens_ = tokens_[:expr] + [(NAME, "ct_cell_outputs['display_data']"),
                                (OP, "=")] + tokens_[expr:]
    logger.debug("var assigned")
    logger.debug(tokens_)

  return untokenize(tokens_)


def remove_docstring(code):
  """Remove module docstring."""
  tokens = [(x[0], x[1]) for x in _tokenize(code)]
  if tokens[0][0] == STRING and tokens[1][0] == NEWLINE:
    tokens = tokens[2:]
  return untokenize(tokens)


def read_template_dict(code):
  """Read the template file dictionary."""
  # remove docstring
  code = remove_docstring(code)
  code = fully_dedent(code)
  tokens = [(x[0], x[1]) for x in _tokenize(code)]
  # find fist non newline
  # and remove newlines from the beginning
  start = len(tokens)
  for index, token in enumerate(tokens):
    if token[0] not in [NEWLINE, COMMENT, NL]:
      start = index
      break
  tokens = tokens[start:]

  # if it is a dictionary return it
  if tokens[0] == (OP, "{"):
    try:
      return literal_eval(untokenize(tokens))
    except:
      logger.error("Could not evaluate dictionary")
      return None

  logger.error("Unrecognized dictionary")
  return None


def replace_asserts(code):
  """Replace assert."""
  tokens = [(x[0], x[1]) for x in _tokenize(code)]
  tokens_ = []
  in_assert = False
  for token in tokens:
    if token == (NAME, "assert"):
      tokens_.extend([(NAME, "self"), (OP, "."), (NAME, "assertTrue"),
                      (OP, "(")])
      in_assert = True

    elif token[0] == NEWLINE and in_assert:
      tokens_.extend([(OP, ")"), token])
      in_assert = False

    else:
      tokens_.append(token)

  return untokenize(tokens_)


def get_template_file(standard_template, custom_template):
  """Get template file."""
  if custom_template and standard_template:
    raise ValueError("Either choose custom template or standard template")
  standard_files = {
      1: "templates/01_template_default.py",
      2: "templates/02_template_min.py",
  }
  filepath = os.path.join(os.path.dirname(celltest.__file__), standard_files[1])
  if standard_template:
    filepath = os.path.join(
        os.path.dirname(celltest.__file__),
        standard_files[int(standard_template)])
  if custom_template:
    filepath = custom_template
  return filepath


def get_template_from_file(filepath):
  """Get template from file."""
  with open(filepath, "r") as text_file:
    code = text_file.read()
  return read_template_dict(code)


def get_notebook_name():
  """Return the full path of the jupyter notebook."""
  kernel_id = re.search('kernel-(.*).json',
                        ipykernel.connect.get_connection_file()).group(1)
  servers = list_running_servers()
  for server in servers:
    response = requests.get(
        urljoin(server['url'], 'api/sessions'),
        params={'token': server.get('token', '')})
    for response_d in json.loads(response.text):
      if response_d['kernel']['id'] == kernel_id:
        relative_path = response_d['notebook']['path']
        return os.path.join(server['notebook_dir'], relative_path)
  return None


def parse_params(params, accepted_params):
  """Parse cell params."""
  result = {}
  try:
    comment_n = params.index("comment")
  except ValueError:
    comment_n = None
  if comment_n is not None:
    try:
      result["comment"] = params[comment_n + 1]
      params = params[:comment_n] + params[comment_n + 2:]
    except IndexError:
      result["comment"] = ""
      params = params[:comment_n]

  for param in params:
    if param not in accepted_params:
      logger.error("Ignoring unknown param %s", param)
    else:
      result[param] = True

  return result
