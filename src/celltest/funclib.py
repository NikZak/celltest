"""Functions to be used in actual Test suites.

This should be inserted in the test code.
"""
import re
from collections import defaultdict
import logging
import json
from IPython.core.formatters import DisplayFormatter


def escape_ansi(line):
  """Remove colors from error message."""
  ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
  return ansi_escape.sub('', line)


def string_escape(string, encoding='utf-8'):
  """Encode."""
  return '"' + (
      string.encode(
          'unicode-escape')  # Perform the actual octal-escaping encode
      .decode(encoding)).replace('"', '\\"') + '"'  # Decode original encoding


def get_outputs(file_name, pretty_quotes=False):
  """Read outputs from notebook."""
  with open(file_name) as file:
    saved_cell_outputs = defaultdict(lambda: None)
    nb_cells = json.load(file)["cells"]
    for cell_index, cell in enumerate(nb_cells):
      if "outputs" not in cell:
        continue
      saved_cell_outputs[cell_index] = defaultdict(lambda: None)
      for output in cell["outputs"]:
        for stream in ["stdout", "stderr"]:
          if "name" in output and output["name"] == stream:
            saved_cell_outputs[cell_index][stream] = output["text"]
        if "output_type" in output and output[
            "output_type"] == "execute_result" \
                and "data" in output and "text/plain" in output[
                "data"]:
          saved_cell_outputs[cell_index]['display_data'] = output["data"][
              "text/plain"]
      for key, value in saved_cell_outputs[cell_index].items():
        if pretty_quotes:
          if value is not None:
            saved_cell_outputs[cell_index][key] = '(' + "\n".join(
                [string_escape(x) for x in value]) + ')'

        else:
          if value is not None:
            saved_cell_outputs[cell_index][key] = "".join(value)

  return saved_cell_outputs


def capture_log(root_logger, stream):
  """Redirect log."""
  old_handlers = root_logger.handlers
  for handl in old_handlers:
    root_logger.removeHandler(handl)

  handler = logging.StreamHandler(stream)
  handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
  root_logger.addHandler(handler)


def postprocess(cell_outputs, saved_cell_outputs, verbose=True, cell_n=None):
  """Unify outputs and saved_outputs to make them comparable.

  Side effects:
  1) Print outputs
  2) Reinitiate logging object
  """
  if saved_cell_outputs is None:
    saved_cell_outputs = defaultdict(lambda: None)

  cell_outputs["stderr"], cell_outputs["stdout"] = cell_outputs[
      "stderr"].getvalue(), cell_outputs["stdout"].getvalue()
  if verbose:
    print(
        "-----> stderr of Cell %d:" % cell_n,
        cell_outputs["stderr"],
        "-----> stdout of Cell %d:" % cell_n,
        cell_outputs["stdout"],
        sep="\n")
  root_logger = logging.getLogger()

  # Reinitiate the logging object
  for handl in root_logger.handlers:
    root_logger.removeHandler(handl)
  logging.basicConfig()

  if saved_cell_outputs["stdout"] is None:
    saved_cell_outputs["stdout"] = ''

  if saved_cell_outputs["stderr"] is None:
    saved_cell_outputs["stderr"] = ''

  cell_outputs["stderr"] = escape_ansi(cell_outputs["stderr"])

  if cell_outputs["display_data"] is None:
    cell_outputs["display_data"] = ''
  if saved_cell_outputs["display_data"] is None:
    saved_cell_outputs["display_data"] = "''"
  # elif isinstance(cell_outputs, str):
  #   cell_outputs = "'" + cell_outputs + "'"

  celltest_disp = DisplayFormatter()
  cell_outputs["display_data"] = celltest_disp.format(
      cell_outputs["display_data"], include="text/plain")[0]['text/plain']

  return cell_outputs, saved_cell_outputs
