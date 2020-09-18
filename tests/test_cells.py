"""Tests automatically generated from notebook cells.ipynb.

Do not make direct changes in this file as it may be
regenerated, make all changes in the notebook.

Accepted parameters in notebook cells to control test flow:
['comment', 'setup', 'ignore_outputs', 'ignore_stderr', 'ignore_stdout', 'ignore', 'ignore_display_data', 'run_all_till_now']

Accepted callbacks (if installed) to prettify the .py test file:
black, yapf, isort

To change the test file default copy and change the template.py from
celltest/src/celltest.
"""
import io
import json
import logging
import os
import re
from collections import defaultdict
from contextlib import redirect_stderr, redirect_stdout
from tokenize import untokenize
from unittest import TestCase, main

from IPython.core.formatters import DisplayFormatter

import celltest
from celltest.cells import CellConvert
from celltest.utils import _tokenize, fully_dedent, indent, parse_params, save_outputs


def escape_ansi(line):
  """Remove colors from error message."""
  ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
  return ansi_escape.sub("", line)


def string_escape(string, encoding="utf-8"):
  """Encode."""
  return ('"' + (
      string.encode(
          "unicode-escape").decode(  # Perform the actual octal-escaping encode
              encoding)).replace('"', '\\"') + '"')  # Decode original encoding


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
        if ("output_type" in output and
            output["output_type"] == "execute_result" and "data" in output and
            "text/plain" in output["data"]):
          saved_cell_outputs[cell_index]["display_data"] = output["data"][
              "text/plain"]
      for key, value in saved_cell_outputs[cell_index].items():
        if pretty_quotes:
          if value is not None:
            saved_cell_outputs[cell_index][key] = (
                "(" + "\n".join([string_escape(x) for x in value]) + ")")

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

  cell_outputs["stderr"], cell_outputs["stdout"] = (
      cell_outputs["stderr"].getvalue(),
      cell_outputs["stdout"].getvalue(),
  )
  if verbose:
    print(
        "-----> stderr of Cell %d:" % cell_n,
        cell_outputs["stderr"],
        "-----> stdout of Cell %d:" % cell_n,
        cell_outputs["stdout"],
        sep="\n",
    )
  root_logger = logging.getLogger()

  # Reinitiate the logging object
  for handl in root_logger.handlers:
    root_logger.removeHandler(handl)
  logging.basicConfig()

  if saved_cell_outputs["stdout"] is None:
    saved_cell_outputs["stdout"] = ""

  if saved_cell_outputs["stderr"] is None:
    saved_cell_outputs["stderr"] = ""

  cell_outputs["stderr"] = escape_ansi(cell_outputs["stderr"])

  if cell_outputs["display_data"] is None:
    cell_outputs["display_data"] = ""
  if saved_cell_outputs["display_data"] is None:
    saved_cell_outputs["display_data"] = "''"
    # elif isinstance(cell_outputs, str):
    #   cell_outputs = "'" + cell_outputs + "'"

  celltest_disp = DisplayFormatter()
  cell_outputs["display_data"] = celltest_disp.format(
      cell_outputs["display_data"], include="text/plain")[0]["text/plain"]

  return cell_outputs, saved_cell_outputs


root_logger = logging.getLogger()
if not root_logger.handlers:
  logging.basicConfig()

TestCase.maxDiff = None
if os.path.exists(os.path.join(os.getcwd(), "tests")):
  cellconvert = CellConvert(filepath="tests/example.ipynb")
else:
  cellconvert = CellConvert(filepath="example.ipynb")
test = """ return0()
        if (
            '2'
            ):
            True
        if True:
            1
            m
        else:
            3
        pdb.debug()    
        a = 3
        m
        # some comment

"""
test2 = """

        return0()
        a = 2
        if ('2'):
            True
        if True:
            1
        else:
            3
        m

"""
test3 = """
df. head()
"""

untokenize([(x[0], x[1]) for x in _tokenize(test)])


class Test(TestCase):
  """Test class."""

  def test_00003(self, verbose=True):
    """Test cell 3."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs[
        "stderr"] = "ERROR:celltest:Ignoring unknown param test_param\n"
    ct_saved_cell_outputs[
        "display_data"] = "{'comment': 'ssdfsdfsd dfsdf ', 'ignore': True}"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 3 code
      ct_cell_outputs["display_data"] = parse_params(
          ["test_param", "comment", "ssdfsdfsd dfsdf ", "ignore"],
          ["ignore", "ignore_outputs"],
      )
      # >>>>>>> End of Cell 3 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=3)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00004(self, verbose=True):
    """Test cell 4."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs[
        "display_data"] = "'[TokenInfo(type=54 (OP), string=\\'{\\', start=(1, 0), end=(1, 1), line=\"{\\'a\\'}\\\\n\"),\\n TokenInfo(type=3 (STRING), string=\"\\'a\\'\", start=(1, 1), end=(1, 4), line=\"{\\'a\\'}\\\\n\"),\\n TokenInfo(type=54 (OP), string=\\'}\\', start=(1, 4), end=(1, 5), line=\"{\\'a\\'}\\\\n\"),\\n TokenInfo(type=4 (NEWLINE), string=\\'\\\\n\\', start=(1, 5), end=(1, 6), line=\"{\\'a\\'}\\\\n\"),\\n TokenInfo(type=54 (OP), string=\\'[\\', start=(2, 0), end=(2, 1), line=\"[\\'a\\']\"),\\n TokenInfo(type=3 (STRING), string=\"\\'a\\'\", start=(2, 1), end=(2, 4), line=\"[\\'a\\']\"),\\n TokenInfo(type=54 (OP), string=\\']\\', start=(2, 4), end=(2, 5), line=\"[\\'a\\']\"),\\n TokenInfo(type=4 (NEWLINE), string=\\'\\', start=(2, 5), end=(2, 6), line=\\'\\'),\\n TokenInfo(type=0 (ENDMARKER), string=\\'\\', start=(3, 0), end=(3, 0), line=\\'\\')]'"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 4 code
      d = DisplayFormatter()
      ct_cell_outputs["display_data"] = d.format(
          [x for x in _tokenize("""{'a'}
['a']""")],
          include="text/plain",
      )[0]["text/plain"]
      # >>>>>>> End of Cell 4 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=4)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00006(self, verbose=True):
    """Test cell 6."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "{1: '# CT: ignore_outputs\\nimport pandas as pd\\nimport tokenize, \\\\\\nio\\nimport os\\nimport logging',\n"
        " 3: '# CT: ignore, some_giberish\\nos.path.join?',\n"
        " 4: '# CT: setup\\ndf = pd.read_json(\"https://data.smcgov.org/resource/mb6a-xn89.json\")',\n"
        ' 5: \'logging.error("test")\\nlogging.error("test")\\nprint("test")\\nlogging.error("test")\\nprint("test")\',\n'
        ' 6: \'# CT: param1, param2; param3\\nprint("Hello World")\\nprint("Hello World")\\nlogging.error("test")\\nlogging.error("test")\\nprint("test")\\nlogging.error("test")\',\n'
        " 7: 'print(\"Hello World\")',\n"
        " 8: 'df.head(5)',\n"
        " 9: 'df.shape',\n"
        " 10: '# CT: ignore_outputs\\ndf.describe()',\n"
        ' 11: \'df.drop("location_1", axis=1).describe(include="all")\',\n'
        " 12: 'df.dtypes',\n"
        " 13: '# CT: almost_equal\\ndf.bachelor_s_degree_or_higher.mean()',\n"
        " 14: 'df.geography.count()',\n"
        " 15: 'df.geography_type.unique()',\n"
        " 16: 'df.less_than_high_school_graduate.value_counts()',\n"
        ' 18: \'"a   ...  b".split(" ")\',\n'
        " 19: '\"\" is \\'\\'',\n"
        " 20: '\" \"*4',\n"
        " 21: 'None',\n"
        " 22: 'str(True)',\n"
        " 23: \"'''True''' == str(True)\"}")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 6 code
      ct_cell_outputs["display_data"] = cellconvert.code_d_
      # >>>>>>> End of Cell 6 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=6)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00007(self, verbose=True):
    """Test cell 7."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs[
        "display_data"] = "{3: ['ignore'], 4: ['setup'], 5: ['setup'], 7: ['ignore_output']}"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 7 code
      ct_cell_outputs["display_data"] = cellconvert.metadata_d
      # >>>>>>> End of Cell 7 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=7)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00008(self, verbose=True):
    """Test cell 8."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "{1: '# CT: ignore_outputs\\nimport pandas as pd\\nimport tokenize,  io\\nimport os\\nimport logging',\n"
        " 3: '# CT: ignore, some_giberish\\nos.path.join?',\n"
        " 4: '# CT: setup\\ndf = pd.read_json(\"https://data.smcgov.org/resource/mb6a-xn89.json\")',\n"
        ' 5: \'logging.error("test")\\nlogging.error("test")\\nprint("test")\\nlogging.error("test")\\nprint("test")\',\n'
        ' 6: \'# CT: param1, param2; param3\\nprint("Hello World")\\nprint("Hello World")\\nlogging.error("test")\\nlogging.error("test")\\nprint("test")\\nlogging.error("test")\',\n'
        " 7: 'print(\"Hello World\")',\n"
        " 8: 'df.head(5)',\n"
        " 9: 'df.shape',\n"
        " 10: '# CT: ignore_outputs\\ndf.describe()',\n"
        ' 11: \'df.drop("location_1", axis=1).describe(include="all")\',\n'
        " 12: 'df.dtypes',\n"
        " 13: '# CT: almost_equal\\ndf.bachelor_s_degree_or_higher.mean()',\n"
        " 14: 'df.geography.count()',\n"
        " 15: 'df.geography_type.unique()',\n"
        " 16: 'df.less_than_high_school_graduate.value_counts()',\n"
        ' 18: \'"a   ...  b".split(" ")\',\n'
        " 19: '\"\" is \\'\\'',\n"
        " 20: '\" \"*4',\n"
        " 21: 'None',\n"
        " 22: 'str(True)',\n"
        " 23: \"'''True''' == str(True)\"}")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 8 code
      ct_cell_outputs["display_data"] = cellconvert.remove_backslash()
      # >>>>>>> End of Cell 8 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=8)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00009(self, verbose=True):
    """Test cell 9."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "({},\n"
        " {1: '# CT: ignore_outputs\\nimport pandas as pd\\nimport tokenize,  io\\nimport os\\nimport logging',\n"
        "  3: '# CT: ignore, some_giberish\\nos.path.join?',\n"
        "  4: '# CT: setup\\ndf = pd.read_json(\"https://data.smcgov.org/resource/mb6a-xn89.json\")',\n"
        '  5: \'logging.error("test")\\nlogging.error("test")\\nprint("test")\\nlogging.error("test")\\nprint("test")\',\n'
        '  6: \'# CT: param1, param2; param3\\nprint("Hello World")\\nprint("Hello World")\\nlogging.error("test")\\nlogging.error("test")\\nprint("test")\\nlogging.error("test")\',\n'
        "  7: 'print(\"Hello World\")',\n"
        "  8: 'df.head(5)',\n"
        "  9: 'df.shape',\n"
        "  10: '# CT: ignore_outputs\\ndf.describe()',\n"
        '  11: \'df.drop("location_1", axis=1).describe(include="all")\',\n'
        "  12: 'df.dtypes',\n"
        "  13: '# CT: almost_equal\\ndf.bachelor_s_degree_or_higher.mean()',\n"
        "  14: 'df.geography.count()',\n"
        "  15: 'df.geography_type.unique()',\n"
        "  16: 'df.less_than_high_school_graduate.value_counts()',\n"
        '  18: \'"a   ...  b".split(" ")\',\n'
        "  19: '\"\" is \\'\\'',\n"
        "  20: '\" \"*4',\n"
        "  21: 'None',\n"
        "  22: 'str(True)',\n"
        "  23: \"'''True''' == str(True)\"})")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 9 code
      ct_cell_outputs["display_data"] = cellconvert.carve_magic()
      # >>>>>>> End of Cell 9 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=9)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00010(self, verbose=True):
    """Test cell 10."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = (
        "ERROR:celltest:Ignoring unknown param ignore_output\n"
        "ERROR:celltest:Ignoring unknown param ignore,\n"
        "ERROR:celltest:Ignoring unknown param some_giberish\n"
        "ERROR:celltest:Ignoring unknown param param1,\n"
        "ERROR:celltest:Ignoring unknown param param2;\n"
        "ERROR:celltest:Ignoring unknown param param3\n"
        "ERROR:celltest:Ignoring unknown param almost_equal\n")
    ct_saved_cell_outputs["display_data"] = (
        "defaultdict(dict,\n"
        "            {'head_level': {'insert_saved_outputs': True},\n"
        "             3: {'ignore': True},\n"
        "             4: {'setup': True},\n"
        "             5: {'setup': True},\n"
        "             7: {},\n"
        "             1: {'ignore_outputs': True},\n"
        "             6: {},\n"
        "             8: {},\n"
        "             9: {},\n"
        "             10: {'ignore_outputs': True},\n"
        "             11: {},\n"
        "             12: {},\n"
        "             13: {},\n"
        "             14: {},\n"
        "             15: {},\n"
        "             16: {},\n"
        "             18: {},\n"
        "             19: {},\n"
        "             20: {},\n"
        "             21: {},\n"
        "             22: {},\n"
        "             23: {}})")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 10 code
      ct_cell_outputs["display_data"] = cellconvert.carve_control_params()
      # >>>>>>> End of Cell 10 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=10)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00011(self, verbose=True):
    """Test cell 11."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "('import pandas as pd \\nimport tokenize ,io \\nimport os \\nimport logging \\n',\n"
        " {1: '',\n"
        "  4: 'df =pd .read_json (\"https://data.smcgov.org/resource/mb6a-xn89.json\")',\n"
        '  5: \'logging .error ("test")\\nlogging .error ("test")\\nprint ("test")\\nlogging .error ("test")\\nprint ("test")\',\n'
        '  6: \'print ("Hello World")\\nprint ("Hello World")\\nlogging .error ("test")\\nlogging .error ("test")\\nprint ("test")\\nlogging .error ("test")\',\n'
        "  7: 'print (\"Hello World\")',\n"
        "  8: 'df .head (5 )',\n"
        "  9: 'df .shape ',\n"
        "  10: 'df .describe ()',\n"
        '  11: \'df .drop ("location_1",axis =1 ).describe (include ="all")\',\n'
        "  12: 'df .dtypes ',\n"
        "  13: 'df .bachelor_s_degree_or_higher .mean ()',\n"
        "  14: 'df .geography .count ()',\n"
        "  15: 'df .geography_type .unique ()',\n"
        "  16: 'df .less_than_high_school_graduate .value_counts ()',\n"
        '  18: \'"a   ...  b".split (" ")\',\n'
        "  19: '\"\"is \\'\\'',\n"
        "  20: '\" \"*4 ',\n"
        "  21: 'None ',\n"
        "  22: 'str (True )',\n"
        "  23: \"'''True'''==str (True )\"})")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 11 code
      ct_cell_outputs["display_data"] = cellconvert.carve_imports()
      # >>>>>>> End of Cell 11 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=11)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00012(self, verbose=True):
    """Test cell 12."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        '(\'df =pd .read_json ("https://data.smcgov.org/resource/mb6a-xn89.json")\\nlogging .error ("test")\\nlogging .error ("test")\\nprint ("test")\\nlogging .error ("test")\\nprint ("test")\',\n'
        " {1: '',\n"
        '  6: \'print ("Hello World")\\nprint ("Hello World")\\nlogging .error ("test")\\nlogging .error ("test")\\nprint ("test")\\nlogging .error ("test")\',\n'
        "  7: 'print (\"Hello World\")',\n"
        "  8: 'df .head (5 )',\n"
        "  9: 'df .shape ',\n"
        "  10: 'df .describe ()',\n"
        '  11: \'df .drop ("location_1",axis =1 ).describe (include ="all")\',\n'
        "  12: 'df .dtypes ',\n"
        "  13: 'df .bachelor_s_degree_or_higher .mean ()',\n"
        "  14: 'df .geography .count ()',\n"
        "  15: 'df .geography_type .unique ()',\n"
        "  16: 'df .less_than_high_school_graduate .value_counts ()',\n"
        '  18: \'"a   ...  b".split (" ")\',\n'
        "  19: '\"\"is \\'\\'',\n"
        "  20: '\" \"*4 ',\n"
        "  21: 'None ',\n"
        "  22: 'str (True )',\n"
        "  23: \"'''True'''==str (True )\"})")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 12 code
      ct_cell_outputs["display_data"] = cellconvert.carve_setup()
      # >>>>>>> End of Cell 12 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=12)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00013(self, verbose=True):
    """Test cell 13."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs[
        "display_data"] = "'\\n        import pandas \\n        test =Dataframe ()\\n        for i in range (10 ):\\n            i +=1 \\n'"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 13 code
      ct_cell_outputs["display_data"] = indent("""
    import pandas
    test = Dataframe()
    for i in range(10):
        i +=1
""")
      # >>>>>>> End of Cell 13 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=13)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00015(self, verbose=True):
    """Test cell 15."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs[
        "display_data"] = "\"return0 ()\\n        if (\\n        '2'\\n        ):\\n            True \\n        if True :\\n            1 \\n            m \\n        else :\\n            3 \\n        pdb .debug ()\\n        a =3 \\n        m \\n        # some comment\\n\\n\""

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 15 code
      ct_cell_outputs["display_data"] = fully_dedent(test)
      # >>>>>>> End of Cell 15 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=15)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00016(self, verbose=True):
    """Test cell 16."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "[TokenInfo(type=1 (NAME), string='return0', start=(1, 0), end=(1, 7), line='return0 ()\\n'),\n"
        " TokenInfo(type=54 (OP), string='(', start=(1, 8), end=(1, 9), line='return0 ()\\n'),\n"
        " TokenInfo(type=54 (OP), string=')', start=(1, 9), end=(1, 10), line='return0 ()\\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(1, 10), end=(1, 11), line='return0 ()\\n'),\n"
        " TokenInfo(type=5 (INDENT), string='        ', start=(2, 0), end=(2, 8), line='        if (\\n'),\n"
        " TokenInfo(type=1 (NAME), string='if', start=(2, 8), end=(2, 10), line='        if (\\n'),\n"
        " TokenInfo(type=54 (OP), string='(', start=(2, 11), end=(2, 12), line='        if (\\n'),\n"
        " TokenInfo(type=61 (NL), string='\\n', start=(2, 12), end=(2, 13), line='        if (\\n'),\n"
        " TokenInfo(type=3 (STRING), string=\"'2'\", start=(3, 8), end=(3, 11), line=\"        '2'\\n\"),\n"
        " TokenInfo(type=61 (NL), string='\\n', start=(3, 11), end=(3, 12), line=\"        '2'\\n\"),\n"
        " TokenInfo(type=54 (OP), string=')', start=(4, 8), end=(4, 9), line='        ):\\n'),\n"
        " TokenInfo(type=54 (OP), string=':', start=(4, 9), end=(4, 10), line='        ):\\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(4, 10), end=(4, 11), line='        ):\\n'),\n"
        " TokenInfo(type=5 (INDENT), string='            ', start=(5, 0), end=(5, 12), line='            True \\n'),\n"
        " TokenInfo(type=1 (NAME), string='True', start=(5, 12), end=(5, 16), line='            True \\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(5, 17), end=(5, 18), line='            True \\n'),\n"
        " TokenInfo(type=6 (DEDENT), string='', start=(6, 8), end=(6, 8), line='        if True :\\n'),\n"
        " TokenInfo(type=1 (NAME), string='if', start=(6, 8), end=(6, 10), line='        if True :\\n'),\n"
        " TokenInfo(type=1 (NAME), string='True', start=(6, 11), end=(6, 15), line='        if True :\\n'),\n"
        " TokenInfo(type=54 (OP), string=':', start=(6, 16), end=(6, 17), line='        if True :\\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(6, 17), end=(6, 18), line='        if True :\\n'),\n"
        " TokenInfo(type=5 (INDENT), string='            ', start=(7, 0), end=(7, 12), line='            1 \\n'),\n"
        " TokenInfo(type=2 (NUMBER), string='1', start=(7, 12), end=(7, 13), line='            1 \\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(7, 14), end=(7, 15), line='            1 \\n'),\n"
        " TokenInfo(type=1 (NAME), string='m', start=(8, 12), end=(8, 13), line='            m \\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(8, 14), end=(8, 15), line='            m \\n'),\n"
        " TokenInfo(type=6 (DEDENT), string='', start=(9, 8), end=(9, 8), line='        else :\\n'),\n"
        " TokenInfo(type=1 (NAME), string='else', start=(9, 8), end=(9, 12), line='        else :\\n'),\n"
        " TokenInfo(type=54 (OP), string=':', start=(9, 13), end=(9, 14), line='        else :\\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(9, 14), end=(9, 15), line='        else :\\n'),\n"
        " TokenInfo(type=5 (INDENT), string='            ', start=(10, 0), end=(10, 12), line='            3 \\n'),\n"
        " TokenInfo(type=2 (NUMBER), string='3', start=(10, 12), end=(10, 13), line='            3 \\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(10, 14), end=(10, 15), line='            3 \\n'),\n"
        " TokenInfo(type=6 (DEDENT), string='', start=(11, 8), end=(11, 8), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=1 (NAME), string='pdb', start=(11, 8), end=(11, 11), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=54 (OP), string='.', start=(11, 12), end=(11, 13), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=1 (NAME), string='debug', start=(11, 13), end=(11, 18), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=54 (OP), string='(', start=(11, 19), end=(11, 20), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=54 (OP), string=')', start=(11, 20), end=(11, 21), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(11, 21), end=(11, 22), line='        pdb .debug ()\\n'),\n"
        " TokenInfo(type=1 (NAME), string='a', start=(12, 8), end=(12, 9), line='        a =3 \\n'),\n"
        " TokenInfo(type=54 (OP), string='=', start=(12, 10), end=(12, 11), line='        a =3 \\n'),\n"
        " TokenInfo(type=2 (NUMBER), string='3', start=(12, 11), end=(12, 12), line='        a =3 \\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(12, 13), end=(12, 14), line='        a =3 \\n'),\n"
        " TokenInfo(type=1 (NAME), string='m', start=(13, 8), end=(13, 9), line='        m \\n'),\n"
        " TokenInfo(type=4 (NEWLINE), string='\\n', start=(13, 10), end=(13, 11), line='        m \\n'),\n"
        " TokenInfo(type=60 (COMMENT), string='# some comment', start=(14, 8), end=(14, 22), line='        # some comment\\n'),\n"
        " TokenInfo(type=61 (NL), string='\\n', start=(14, 22), end=(14, 23), line='        # some comment\\n'),\n"
        " TokenInfo(type=61 (NL), string='\\n', start=(15, 0), end=(15, 1), line='\\n'),\n"
        " TokenInfo(type=6 (DEDENT), string='', start=(16, 0), end=(16, 0), line=''),\n"
        " TokenInfo(type=0 (ENDMARKER), string='', start=(16, 0), end=(16, 0), line='')]"
    )

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 16 code
      ct_cell_outputs["display_data"] = [
          x for x in _tokenize(fully_dedent(test))
      ]
      # >>>>>>> End of Cell 16 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=16)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00017(self, verbose=True):
    """Test cell 17."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = (
        "\n"
        "ct_cell_outputs['display_data'] =df .head ()\n"
        "\n")
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 17 code
      ct_cell_outputs["display_data"] = print(save_outputs(test3))
      # >>>>>>> End of Cell 17 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=17)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00018(self, verbose=True):
    """Test cell 18."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = ("\n"
                                       "\n"
                                       "return0 ()\n"
                                       "a =2 \n"
                                       "if ('2'):\n"
                                       "    True \n"
                                       "if True :\n"
                                       "    1 \n"
                                       "else :\n"
                                       "    3 \n"
                                       "ct_cell_outputs['display_data'] =m \n"
                                       "\n"
                                       "\n")
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 18 code
      ct_cell_outputs["display_data"] = print(save_outputs(test2))
      # >>>>>>> End of Cell 18 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=18)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00019(self, verbose=True):
    """Test cell 19."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = (
        '"""Tests automatically generated from notebook example.ipynb.\n'
        "\n"
        "Do not make direct changes in this file as it may be\n"
        "regenerated, make all changes in the notebook.\n"
        "\n"
        "Accepted parameters in notebook cells to control test flow:\n"
        "['comment', 'setup', 'ignore_outputs', 'ignore_stderr', 'ignore_stdout', 'ignore', 'ignore_display_data', 'run_all_till_now']\n"
        "\n"
        "Accepted callbacks (if installed) to prettify the .py test file:\n"
        "black, yapf, isort\n"
        "\n"
        "To change the test file default copy and change the template.py from\n"
        "celltest/src/celltest.\n"
        '"""\n'
        "from collections import defaultdict\n"
        "import io\n"
        "import logging\n"
        "from contextlib import redirect_stdout, redirect_stderr\n"
        "from unittest import TestCase, main\n"
        "import pandas as pd \n"
        "import tokenize ,io \n"
        "import os \n"
        "import logging \n"
        "\n"
        "\n"
        "import re \n"
        "from collections import defaultdict \n"
        "import logging \n"
        "import json \n"
        "from IPython .core .formatters import DisplayFormatter \n"
        "\n"
        "\n"
        "def escape_ansi (line ):\n"
        '  """Remove colors from error message."""\n'
        "  ansi_escape =re .compile (r'(\\x9B|\\x1B\\[)[0-?]*[ -\\/]*[@-~]')\n"
        "  return ansi_escape .sub ('',line )\n"
        "\n"
        "\n"
        "def string_escape (string ,encoding ='utf-8'):\n"
        '  """Encode."""\n'
        "  return '\"'+(\n"
        "  string .encode (\n"
        "  'unicode-escape')# Perform the actual octal-escaping encode\n"
        "  .decode (encoding )).replace ('\"','\\\\\"')+'\"'# Decode original encoding\n"
        "\n"
        "\n"
        "def get_outputs (file_name ,pretty_quotes =False ):\n"
        '  """Read outputs from notebook."""\n'
        "  with open (file_name )as file :\n"
        "    saved_cell_outputs =defaultdict (lambda :None )\n"
        '    nb_cells =json .load (file )["cells"]\n'
        "    for cell_index ,cell in enumerate (nb_cells ):\n"
        '      if "outputs"not in cell :\n'
        "        continue \n"
        "      saved_cell_outputs [cell_index ]=defaultdict (lambda :None )\n"
        '      for output in cell ["outputs"]:\n'
        '        for stream in ["stdout","stderr"]:\n'
        '          if "name"in output and output ["name"]==stream :\n'
        '            saved_cell_outputs [cell_index ][stream ]=output ["text"]\n'
        '        if "output_type"in output and output [\n'
        '        "output_type"]=="execute_result"and "data"in output and "text/plain"in output [\n'
        '        "data"]:\n'
        "          saved_cell_outputs [cell_index ]['display_data']=output [\"data\"][\n"
        '          "text/plain"]\n'
        "      for key ,value in saved_cell_outputs [cell_index ].items ():\n"
        "        if pretty_quotes :\n"
        "          if value is not None :\n"
        "            saved_cell_outputs [cell_index ][key ]='('+\"\\n\".join (\n"
        "            [string_escape (x )for x in value ])+')'\n"
        "\n"
        "        else :\n"
        "          if value is not None :\n"
        '            saved_cell_outputs [cell_index ][key ]="".join (value )\n'
        "\n"
        "  return saved_cell_outputs \n"
        "\n"
        "\n"
        "def capture_log (root_logger ,stream ):\n"
        '  """Redirect log."""\n'
        "  old_handlers =root_logger .handlers \n"
        "  for handl in old_handlers :\n"
        "    root_logger .removeHandler (handl )\n"
        "\n"
        "  handler =logging .StreamHandler (stream )\n"
        "  handler .setFormatter (logging .Formatter (logging .BASIC_FORMAT ))\n"
        "  root_logger .addHandler (handler )\n"
        "\n"
        "\n"
        "def postprocess (cell_outputs ,saved_cell_outputs ,verbose =True ,cell_n =None ):\n"
        '  """Unify outputs and saved_outputs to make them comparable.\n'
        "\n"
        "  Side effects:\n"
        "  1) Print outputs\n"
        "  2) Reinitiate logging object\n"
        '  """\n'
        "  if saved_cell_outputs is None :\n"
        "    saved_cell_outputs =defaultdict (lambda :None )\n"
        "\n"
        '  cell_outputs ["stderr"],cell_outputs ["stdout"]=cell_outputs [\n'
        '  "stderr"].getvalue (),cell_outputs ["stdout"].getvalue ()\n'
        "  if verbose :\n"
        "    print (\n"
        '    "-----> stderr of Cell %d:"%cell_n ,\n'
        '    cell_outputs ["stderr"],\n'
        '    "-----> stdout of Cell %d:"%cell_n ,\n'
        '    cell_outputs ["stdout"],\n'
        '    sep ="\\n")\n'
        "  root_logger =logging .getLogger ()\n"
        "\n"
        "  # Reinitiate the logging object\n"
        "  for handl in root_logger .handlers :\n"
        "    root_logger .removeHandler (handl )\n"
        "  logging .basicConfig ()\n"
        "\n"
        '  if saved_cell_outputs ["stdout"]is None :\n'
        "    saved_cell_outputs [\"stdout\"]=''\n"
        "\n"
        '  if saved_cell_outputs ["stderr"]is None :\n'
        "    saved_cell_outputs [\"stderr\"]=''\n"
        "\n"
        '  cell_outputs ["stderr"]=escape_ansi (cell_outputs ["stderr"])\n'
        "\n"
        '  if cell_outputs ["display_data"]is None :\n'
        "    cell_outputs [\"display_data\"]=''\n"
        '  if saved_cell_outputs ["display_data"]is None :\n'
        '    saved_cell_outputs ["display_data"]="\'\'"\n'
        "    # elif isinstance(cell_outputs, str):\n"
        '    #   cell_outputs = "\'" + cell_outputs + "\'"\n'
        "\n"
        "  celltest_disp =DisplayFormatter ()\n"
        '  cell_outputs ["display_data"]=celltest_disp .format (\n'
        '  cell_outputs ["display_data"],include ="text/plain")[0 ][\'text/plain\']\n'
        "\n"
        "  return cell_outputs ,saved_cell_outputs \n"
        "\n"
        "\n"
        "root_logger = logging.getLogger()\n"
        "if not root_logger.handlers:\n"
        "    logging.basicConfig()\n"
        "\n"
        "TestCase.maxDiff = None\n"
        'df =pd .read_json ("https://data.smcgov.org/resource/mb6a-xn89.json")\n'
        'logging .error ("test")\n'
        'logging .error ("test")\n'
        'print ("test")\n'
        'logging .error ("test")\n'
        'print ("test")\n'
        "\n"
        "class Test(TestCase):\n"
        '    """Test class."""\n'
        "\n"
        "    def test_00006(self, verbose=True):\n"
        '        """Test cell 6."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = ("Hello World\\n"\n'
        '"Hello World\\n"\n'
        '"test\\n")\n'
        '        ct_saved_cell_outputs["stderr"] = ("ERROR:root:test\\n"\n'
        '"ERROR:root:test\\n"\n'
        '"ERROR:root:test\\n")\n'
        '        ct_saved_cell_outputs["display_data"] = None\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 6 code\n"
        '            print ("Hello World")\n'
        '            print ("Hello World")\n'
        '            logging .error ("test")\n'
        '            logging .error ("test")\n'
        '            print ("test")\n'
        "            ct_cell_outputs ['display_data']=logging .error (\"test\")\n"
        "            # >>>>>>> End of Cell 6 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=6)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00007(self, verbose=True):\n"
        '        """Test cell 7."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = ("Hello World\\n")\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = None\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 7 code\n"
        "            ct_cell_outputs ['display_data']=print (\"Hello World\")\n"
        "            # >>>>>>> End of Cell 7 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=7)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00008(self, verbose=True):\n"
        '        """Test cell 8."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("        geography geography_type                     year  \\\\\\n"\n'
        '"0        Atherton           Town  2014-01-01T00:00:00.000   \\n"\n'
        '"1           Colma           Town  2014-01-01T00:00:00.000   \\n"\n'
        '"2     Foster City           City  2014-01-01T00:00:00.000   \\n"\n'
        '"3  Portola Valley           Town  2014-01-01T00:00:00.000   \\n"\n'
        '"4    Redwood City           City  2014-01-01T00:00:00.000   \\n"\n'
        '"\\n"\n'
        '"   less_than_high_school_graduate  high_school_graduate  \\\\\\n"\n'
        '"0                            13.6                  12.3   \\n"\n'
        '"1                             6.3                   6.4   \\n"\n'
        '"2                            11.9                   9.7   \\n"\n'
        '"3                            48.1                   0.0   \\n"\n'
        '"4                            16.4                  10.6   \\n"\n'
        '"\\n"\n'
        '"   some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\\\\n"\n'
        '"0                                 2.7                          3.5   \\n"\n'
        '"1                                10.4                          2.4   \\n"\n'
        '"2                                 2.0                          2.9   \\n"\n'
        '"3                                 0.0                          1.8   \\n"\n'
        '"4                                 6.6                          3.0   \\n"\n'
        '"\\n"\n'
        '"                                          location_1  \\\\\\n"\n'
        "\"0  {'type': 'Point', 'coordinates': [-122.2, 37.4...   \\n\"\n"
        "\"1  {'type': 'Point', 'coordinates': [-122.455556,...   \\n\"\n"
        "\"2  {'type': 'Point', 'coordinates': [-122.266389,...   \\n\"\n"
        "\"3  {'type': 'Point', 'coordinates': [-122.218611,...   \\n\"\n"
        "\"4  {'type': 'Point', 'coordinates': [-122.236111,...   \\n\"\n"
        '"\\n"\n'
        '"   :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \\n"\n'
        '"0                          2.0                        28596  \\n"\n'
        '"1                          4.0                        28588  \\n"\n'
        '"2                          6.0                          319  \\n"\n'
        '"3                         14.0                        28597  \\n"\n'
        '"4                         21.0                        28607  ")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 8 code\n"
        "            ct_cell_outputs ['display_data']=df .head (5 )\n"
        "            # >>>>>>> End of Cell 8 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=8)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00009(self, verbose=True):\n"
        '        """Test cell 9."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("(32, 10)")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 9 code\n"
        "            ct_cell_outputs ['display_data']=df .shape \n"
        "            # >>>>>>> End of Cell 9 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=9)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00010(self, verbose=True):\n"
        '        """Test cell 10."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("       less_than_high_school_graduate  high_school_graduate  \\\\\\n"\n'
        '"count                        32.00000             32.000000   \\n"\n'
        '"mean                         17.80000              6.462500   \\n"\n'
        '"std                          19.29944              4.693905   \\n"\n'
        '"min                           0.00000              0.000000   \\n"\n'
        '"25%                           6.82500              1.925000   \\n"\n'
        '"50%                          13.90000              7.750000   \\n"\n'
        '"75%                          20.97500              9.450000   \\n"\n'
        '"max                         100.00000             16.400000   \\n"\n'
        '"\\n"\n'
        '"       some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\\\\n"\n'
        '"count                           32.000000                    32.000000   \\n"\n'
        '"mean                             5.946875                     2.856250   \\n"\n'
        '"std                              4.728430                     1.873919   \\n"\n'
        '"min                              0.000000                     0.000000   \\n"\n'
        '"25%                              2.525000                     2.100000   \\n"\n'
        '"50%                              5.500000                     3.000000   \\n"\n'
        '"75%                              8.800000                     3.600000   \\n"\n'
        '"max                             18.500000                     9.100000   \\n"\n'
        '"\\n"\n'
        '"       :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \\n"\n'
        '"count                    30.000000                    32.000000  \\n"\n'
        '"mean                     17.733333                 25062.093750  \\n"\n'
        '"std                       9.762466                  9502.711577  \\n"\n'
        '"min                       1.000000                   312.000000  \\n"\n'
        '"25%                       9.500000                 28587.750000  \\n"\n'
        '"50%                      18.500000                 28595.000000  \\n"\n'
        '"75%                      25.750000                 28604.250000  \\n"\n'
        '"max                      34.000000                 28613.000000  ")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 10 code\n"
        "            ct_cell_outputs ['display_data']=df .describe ()\n"
        "            # >>>>>>> End of Cell 10 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=10)\n"
        "\n"
        "    def test_00011(self, verbose=True):\n"
        '        """Test cell 11."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("            geography geography_type                     year  \\\\\\n"\n'
        '"count              32             32                       32   \\n"\n'
        '"unique             32              3                        1   \\n"\n'
        '"top     Half Moon Bay           City  2014-01-01T00:00:00.000   \\n"\n'
        '"freq                1             15                       32   \\n"\n'
        '"mean              NaN            NaN                      NaN   \\n"\n'
        '"std               NaN            NaN                      NaN   \\n"\n'
        '"min               NaN            NaN                      NaN   \\n"\n'
        '"25%               NaN            NaN                      NaN   \\n"\n'
        '"50%               NaN            NaN                      NaN   \\n"\n'
        '"75%               NaN            NaN                      NaN   \\n"\n'
        '"max               NaN            NaN                      NaN   \\n"\n'
        '"\\n"\n'
        '"        less_than_high_school_graduate  high_school_graduate  \\\\\\n"\n'
        '"count                         32.00000             32.000000   \\n"\n'
        '"unique                             NaN                   NaN   \\n"\n'
        '"top                                NaN                   NaN   \\n"\n'
        '"freq                               NaN                   NaN   \\n"\n'
        '"mean                          17.80000              6.462500   \\n"\n'
        '"std                           19.29944              4.693905   \\n"\n'
        '"min                            0.00000              0.000000   \\n"\n'
        '"25%                            6.82500              1.925000   \\n"\n'
        '"50%                           13.90000              7.750000   \\n"\n'
        '"75%                           20.97500              9.450000   \\n"\n'
        '"max                          100.00000             16.400000   \\n"\n'
        '"\\n"\n'
        '"        some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\\\\n"\n'
        '"count                            32.000000                    32.000000   \\n"\n'
        '"unique                                 NaN                          NaN   \\n"\n'
        '"top                                    NaN                          NaN   \\n"\n'
        '"freq                                   NaN                          NaN   \\n"\n'
        '"mean                              5.946875                     2.856250   \\n"\n'
        '"std                               4.728430                     1.873919   \\n"\n'
        '"min                               0.000000                     0.000000   \\n"\n'
        '"25%                               2.525000                     2.100000   \\n"\n'
        '"50%                               5.500000                     3.000000   \\n"\n'
        '"75%                               8.800000                     3.600000   \\n"\n'
        '"max                              18.500000                     9.100000   \\n"\n'
        '"\\n"\n'
        '"        :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \\n"\n'
        '"count                     30.000000                    32.000000  \\n"\n'
        '"unique                          NaN                          NaN  \\n"\n'
        '"top                             NaN                          NaN  \\n"\n'
        '"freq                            NaN                          NaN  \\n"\n'
        '"mean                      17.733333                 25062.093750  \\n"\n'
        '"std                        9.762466                  9502.711577  \\n"\n'
        '"min                        1.000000                   312.000000  \\n"\n'
        '"25%                        9.500000                 28587.750000  \\n"\n'
        '"50%                       18.500000                 28595.000000  \\n"\n'
        '"75%                       25.750000                 28604.250000  \\n"\n'
        '"max                       34.000000                 28613.000000  ")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 11 code\n"
        '            ct_cell_outputs [\'display_data\']=df .drop ("location_1",axis =1 ).describe (include ="all")\n'
        "            # >>>>>>> End of Cell 11 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=11)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00012(self, verbose=True):\n"
        '        """Test cell 12."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("geography                              object\\n"\n'
        '"geography_type                         object\\n"\n'
        '"year                                   object\\n"\n'
        '"less_than_high_school_graduate        float64\\n"\n'
        '"high_school_graduate                  float64\\n"\n'
        '"some_college_or_associate_s_degree    float64\\n"\n'
        '"bachelor_s_degree_or_higher           float64\\n"\n'
        '"location_1                             object\\n"\n'
        '":@computed_region_uph5_8hpn           float64\\n"\n'
        '":@computed_region_i2t2_cryp             int64\\n"\n'
        '"dtype: object")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 12 code\n"
        "            ct_cell_outputs ['display_data']=df .dtypes \n"
        "            # >>>>>>> End of Cell 12 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=12)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00013(self, verbose=True):\n"
        '        """Test cell 13."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("2.85625")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 13 code\n"
        "            ct_cell_outputs ['display_data']=df .bachelor_s_degree_or_higher .mean ()\n"
        "            # >>>>>>> End of Cell 13 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=13)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00014(self, verbose=True):\n"
        '        """Test cell 14."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("32")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 14 code\n"
        "            ct_cell_outputs ['display_data']=df .geography .count ()\n"
        "            # >>>>>>> End of Cell 14 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=14)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00015(self, verbose=True):\n"
        '        """Test cell 15."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        "        ct_saved_cell_outputs[\"display_data\"] = (\"array(['Town', 'City', 'CDP'], dtype=object)\")\n"
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 15 code\n"
        "            ct_cell_outputs ['display_data']=df .geography_type .unique ()\n"
        "            # >>>>>>> End of Cell 15 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=15)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00016(self, verbose=True):\n"
        '        """Test cell 16."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("0.0      4\\n"\n'
        '"14.2     1\\n"\n'
        '"8.5      1\\n"\n'
        '"7.0      1\\n"\n'
        '"100.0    1\\n"\n'
        '"9.5      1\\n"\n'
        '"11.9     1\\n"\n'
        '"4.8      1\\n"\n'
        '"31.1     1\\n"\n'
        '"26.7     1\\n"\n'
        '"6.2      1\\n"\n'
        '"15.7     1\\n"\n'
        '"22.1     1\\n"\n'
        '"16.4     1\\n"\n'
        '"6.3      1\\n"\n'
        '"44.4     1\\n"\n'
        '"20.9     1\\n"\n'
        '"7.7      1\\n"\n'
        '"9.2      1\\n"\n'
        '"37.8     1\\n"\n'
        '"3.3      1\\n"\n'
        '"15.1     1\\n"\n'
        '"48.1     1\\n"\n'
        '"18.3     1\\n"\n'
        '"21.2     1\\n"\n'
        '"16.1     1\\n"\n'
        '"13.6     1\\n"\n'
        '"13.4     1\\n"\n'
        '"20.1     1\\n"\n'
        '"Name: less_than_high_school_graduate, dtype: int64")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 16 code\n"
        "            ct_cell_outputs ['display_data']=df .less_than_high_school_graduate .value_counts ()\n"
        "            # >>>>>>> End of Cell 16 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=16)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00018(self, verbose=True):\n"
        '        """Test cell 18."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        "        ct_saved_cell_outputs[\"display_data\"] = (\"['a', '', '', '...', '', 'b']\")\n"
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 18 code\n"
        '            ct_cell_outputs [\'display_data\']="a   ...  b".split (" ")\n'
        "            # >>>>>>> End of Cell 18 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=18)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00019(self, verbose=True):\n"
        '        """Test cell 19."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = ("<>:1: SyntaxWarning: \\"is\\" with a literal. Did you mean \\"==\\"?\\n"\n'
        '"<>:1: SyntaxWarning: \\"is\\" with a literal. Did you mean \\"==\\"?\\n"\n'
        '"<ipython-input-38-7e9601f26686>:1: SyntaxWarning: \\"is\\" with a literal. Did you mean \\"==\\"?\\n"\n'
        '"  \\"\\" is \'\'\\n")\n'
        '        ct_saved_cell_outputs["display_data"] = ("True")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 19 code\n"
        "            ct_cell_outputs ['display_data']=\"\"is ''\n"
        "            # >>>>>>> End of Cell 19 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=19)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00020(self, verbose=True):\n"
        '        """Test cell 20."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("\'    \'")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 20 code\n"
        "            ct_cell_outputs ['display_data']=\" \"*4 \n"
        "            # >>>>>>> End of Cell 20 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=20)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00021(self, verbose=True):\n"
        '        """Test cell 21."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = None\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 21 code\n"
        "            ct_cell_outputs ['display_data']=None \n"
        "            # >>>>>>> End of Cell 21 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=21)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00022(self, verbose=True):\n"
        '        """Test cell 22."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("\'True\'")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 22 code\n"
        "            ct_cell_outputs ['display_data']=str (True )\n"
        "            # >>>>>>> End of Cell 22 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=22)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "    def test_00023(self, verbose=True):\n"
        '        """Test cell 23."""\n'
        "        ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "        ct_saved_cell_outputs = defaultdict(lambda :None)\n"
        '        ct_saved_cell_outputs["stdout"] = None\n'
        '        ct_saved_cell_outputs["stderr"] = None\n'
        '        ct_saved_cell_outputs["display_data"] = ("True")\n'
        "\n"
        '        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(\n'
        "        )\n"
        '        capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '            ct_cell_outputs["stderr"]):\n'
        "\n"
        "            # <<<<<<< Cell 23 code\n"
        "            ct_cell_outputs ['display_data']='''True'''==str (True )\n"
        "            # >>>>>>> End of Cell 23 code\n"
        "\n"
        "        ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=23)\n"
        "\n"
        '        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '        self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                           ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
        "\n")
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 19 code
      ct_cell_outputs["display_data"] = print(
          cellconvert.make_tests(update=False,))
      # >>>>>>> End of Cell 19 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=19)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00020(self, verbose=True):
    """Test cell 20."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = (
        '"""Tests automatically generated from notebook example.ipynb.\n'
        "\n"
        "Do not make direct changes in this file as it may be\n"
        "regenerated, make all changes in the notebook.\n"
        "\n"
        "Accepted parameters in notebook cells to control test flow:\n"
        "['comment', 'setup', 'ignore_outputs', 'ignore_stderr', 'ignore_stdout', 'ignore', 'ignore_display_data', 'run_all_till_now']\n"
        "\n"
        "Accepted callbacks (if installed) to prettify the .py test file:\n"
        "black, yapf, isort\n"
        "\n"
        "To change the test file default copy and change the template.py from\n"
        "celltest/src/celltest.\n"
        '"""\n'
        "from collections import defaultdict\n"
        "import io\n"
        "import logging\n"
        "from contextlib import redirect_stdout, redirect_stderr\n"
        "from unittest import TestCase, main\n"
        "import pandas as pd\n"
        "import tokenize, io\n"
        "import os\n"
        "import logging\n"
        "\n"
        "import re\n"
        "from collections import defaultdict\n"
        "import logging\n"
        "import json\n"
        "from IPython.core.formatters import DisplayFormatter\n"
        "\n"
        "\n"
        "def escape_ansi(line):\n"
        '  """Remove colors from error message."""\n'
        '  ansi_escape = re.compile(r"(\\x9B|\\x1B\\[)[0-?]*[ -\\/]*[@-~]")\n'
        '  return ansi_escape.sub("", line)\n'
        "\n"
        "\n"
        'def string_escape(string, encoding="utf-8"):\n'
        '  """Encode."""\n'
        "  return ('\"' + (\n"
        "      string.encode(\n"
        '          "unicode-escape").decode(  # Perform the actual octal-escaping encode\n'
        "              encoding)).replace('\"', '\\\\\"') + '\"')  # Decode original encoding\n"
        "\n"
        "\n"
        "def get_outputs(file_name, pretty_quotes=False):\n"
        '  """Read outputs from notebook."""\n'
        "  with open(file_name) as file:\n"
        "    saved_cell_outputs = defaultdict(lambda: None)\n"
        '    nb_cells = json.load(file)["cells"]\n'
        "    for cell_index, cell in enumerate(nb_cells):\n"
        '      if "outputs" not in cell:\n'
        "        continue\n"
        "      saved_cell_outputs[cell_index] = defaultdict(lambda: None)\n"
        '      for output in cell["outputs"]:\n'
        '        for stream in ["stdout", "stderr"]:\n'
        '          if "name" in output and output["name"] == stream:\n'
        '            saved_cell_outputs[cell_index][stream] = output["text"]\n'
        '        if ("output_type" in output and\n'
        '            output["output_type"] == "execute_result" and "data" in output and\n'
        '            "text/plain" in output["data"]):\n'
        '          saved_cell_outputs[cell_index]["display_data"] = output["data"][\n'
        '              "text/plain"]\n'
        "      for key, value in saved_cell_outputs[cell_index].items():\n"
        "        if pretty_quotes:\n"
        "          if value is not None:\n"
        "            saved_cell_outputs[cell_index][key] = (\n"
        '                "(" + "\\n".join([string_escape(x) for x in value]) + ")")\n'
        "\n"
        "        else:\n"
        "          if value is not None:\n"
        '            saved_cell_outputs[cell_index][key] = "".join(value)\n'
        "\n"
        "  return saved_cell_outputs\n"
        "\n"
        "\n"
        "def capture_log(root_logger, stream):\n"
        '  """Redirect log."""\n'
        "  old_handlers = root_logger.handlers\n"
        "  for handl in old_handlers:\n"
        "    root_logger.removeHandler(handl)\n"
        "\n"
        "  handler = logging.StreamHandler(stream)\n"
        "  handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))\n"
        "  root_logger.addHandler(handler)\n"
        "\n"
        "\n"
        "def postprocess(cell_outputs, saved_cell_outputs, verbose=True, cell_n=None):\n"
        '  """Unify outputs and saved_outputs to make them comparable.\n'
        "\n"
        "    Side effects:\n"
        "    1) Print outputs\n"
        "    2) Reinitiate logging object\n"
        '    """\n'
        "  if saved_cell_outputs is None:\n"
        "    saved_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        '  cell_outputs["stderr"], cell_outputs["stdout"] = (\n'
        '      cell_outputs["stderr"].getvalue(),\n'
        '      cell_outputs["stdout"].getvalue(),\n'
        "  )\n"
        "  if verbose:\n"
        "    print(\n"
        '        "-----> stderr of Cell %d:" % cell_n,\n'
        '        cell_outputs["stderr"],\n'
        '        "-----> stdout of Cell %d:" % cell_n,\n'
        '        cell_outputs["stdout"],\n'
        '        sep="\\n",\n'
        "    )\n"
        "  root_logger = logging.getLogger()\n"
        "\n"
        "  # Reinitiate the logging object\n"
        "  for handl in root_logger.handlers:\n"
        "    root_logger.removeHandler(handl)\n"
        "  logging.basicConfig()\n"
        "\n"
        '  if saved_cell_outputs["stdout"] is None:\n'
        '    saved_cell_outputs["stdout"] = ""\n'
        "\n"
        '  if saved_cell_outputs["stderr"] is None:\n'
        '    saved_cell_outputs["stderr"] = ""\n'
        "\n"
        '  cell_outputs["stderr"] = escape_ansi(cell_outputs["stderr"])\n'
        "\n"
        '  if cell_outputs["display_data"] is None:\n'
        '    cell_outputs["display_data"] = ""\n'
        '  if saved_cell_outputs["display_data"] is None:\n'
        '    saved_cell_outputs["display_data"] = "\'\'"\n'
        "    # elif isinstance(cell_outputs, str):\n"
        '    #   cell_outputs = "\'" + cell_outputs + "\'"\n'
        "\n"
        "  celltest_disp = DisplayFormatter()\n"
        '  cell_outputs["display_data"] = celltest_disp.format(\n'
        '      cell_outputs["display_data"], include="text/plain")[0]["text/plain"]\n'
        "\n"
        "  return cell_outputs, saved_cell_outputs\n"
        "\n"
        "\n"
        "root_logger = logging.getLogger()\n"
        "if not root_logger.handlers:\n"
        "  logging.basicConfig()\n"
        "\n"
        "TestCase.maxDiff = None\n"
        'df = pd.read_json("https://data.smcgov.org/resource/mb6a-xn89.json")\n'
        'logging.error("test")\n'
        'logging.error("test")\n'
        'print("test")\n'
        'logging.error("test")\n'
        'print("test")\n'
        "\n"
        "\n"
        "class Test(TestCase):\n"
        '  """Test class."""\n'
        "\n"
        "  def test_00006(self, verbose=True):\n"
        '    """Test cell 6."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = "Hello World\\n" "Hello World\\n" "test\\n"\n'
        '    ct_saved_cell_outputs["stderr"] = ("ERROR:root:test\\n"\n'
        '                                       "ERROR:root:test\\n"\n'
        '                                       "ERROR:root:test\\n")\n'
        '    ct_saved_cell_outputs["display_data"] = None\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 6 code\n"
        '      print("Hello World")\n'
        '      print("Hello World")\n'
        '      logging.error("test")\n'
        '      logging.error("test")\n'
        '      print("test")\n'
        '      ct_cell_outputs["display_data"] = logging.error("test")\n'
        "      # >>>>>>> End of Cell 6 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=6)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00007(self, verbose=True):\n"
        '    """Test cell 7."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = "Hello World\\n"\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = None\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 7 code\n"
        '      ct_cell_outputs["display_data"] = print("Hello World")\n'
        "      # >>>>>>> End of Cell 7 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=7)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00008(self, verbose=True):\n"
        '    """Test cell 8."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = (\n'
        '        "        geography geography_type                     year  \\\\\\n"\n'
        '        "0        Atherton           Town  2014-01-01T00:00:00.000   \\n"\n'
        '        "1           Colma           Town  2014-01-01T00:00:00.000   \\n"\n'
        '        "2     Foster City           City  2014-01-01T00:00:00.000   \\n"\n'
        '        "3  Portola Valley           Town  2014-01-01T00:00:00.000   \\n"\n'
        '        "4    Redwood City           City  2014-01-01T00:00:00.000   \\n"\n'
        '        "\\n"\n'
        '        "   less_than_high_school_graduate  high_school_graduate  \\\\\\n"\n'
        '        "0                            13.6                  12.3   \\n"\n'
        '        "1                             6.3                   6.4   \\n"\n'
        '        "2                            11.9                   9.7   \\n"\n'
        '        "3                            48.1                   0.0   \\n"\n'
        '        "4                            16.4                  10.6   \\n"\n'
        '        "\\n"\n'
        '        "   some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\\\\n"\n'
        '        "0                                 2.7                          3.5   \\n"\n'
        '        "1                                10.4                          2.4   \\n"\n'
        '        "2                                 2.0                          2.9   \\n"\n'
        '        "3                                 0.0                          1.8   \\n"\n'
        '        "4                                 6.6                          3.0   \\n"\n'
        '        "\\n"\n'
        '        "                                          location_1  \\\\\\n"\n'
        "        \"0  {'type': 'Point', 'coordinates': [-122.2, 37.4...   \\n\"\n"
        "        \"1  {'type': 'Point', 'coordinates': [-122.455556,...   \\n\"\n"
        "        \"2  {'type': 'Point', 'coordinates': [-122.266389,...   \\n\"\n"
        "        \"3  {'type': 'Point', 'coordinates': [-122.218611,...   \\n\"\n"
        "        \"4  {'type': 'Point', 'coordinates': [-122.236111,...   \\n\"\n"
        '        "\\n"\n'
        '        "   :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \\n"\n'
        '        "0                          2.0                        28596  \\n"\n'
        '        "1                          4.0                        28588  \\n"\n'
        '        "2                          6.0                          319  \\n"\n'
        '        "3                         14.0                        28597  \\n"\n'
        '        "4                         21.0                        28607  ")\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 8 code\n"
        '      ct_cell_outputs["display_data"] = df.head(5)\n'
        "      # >>>>>>> End of Cell 8 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=8)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00009(self, verbose=True):\n"
        '    """Test cell 9."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = "(32, 10)"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 9 code\n"
        '      ct_cell_outputs["display_data"] = df.shape\n'
        "      # >>>>>>> End of Cell 9 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=9)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00010(self, verbose=True):\n"
        '    """Test cell 10."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = (\n'
        '        "       less_than_high_school_graduate  high_school_graduate  \\\\\\n"\n'
        '        "count                        32.00000             32.000000   \\n"\n'
        '        "mean                         17.80000              6.462500   \\n"\n'
        '        "std                          19.29944              4.693905   \\n"\n'
        '        "min                           0.00000              0.000000   \\n"\n'
        '        "25%                           6.82500              1.925000   \\n"\n'
        '        "50%                          13.90000              7.750000   \\n"\n'
        '        "75%                          20.97500              9.450000   \\n"\n'
        '        "max                         100.00000             16.400000   \\n"\n'
        '        "\\n"\n'
        '        "       some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\\\\n"\n'
        '        "count                           32.000000                    32.000000   \\n"\n'
        '        "mean                             5.946875                     2.856250   \\n"\n'
        '        "std                              4.728430                     1.873919   \\n"\n'
        '        "min                              0.000000                     0.000000   \\n"\n'
        '        "25%                              2.525000                     2.100000   \\n"\n'
        '        "50%                              5.500000                     3.000000   \\n"\n'
        '        "75%                              8.800000                     3.600000   \\n"\n'
        '        "max                             18.500000                     9.100000   \\n"\n'
        '        "\\n"\n'
        '        "       :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \\n"\n'
        '        "count                    30.000000                    32.000000  \\n"\n'
        '        "mean                     17.733333                 25062.093750  \\n"\n'
        '        "std                       9.762466                  9502.711577  \\n"\n'
        '        "min                       1.000000                   312.000000  \\n"\n'
        '        "25%                       9.500000                 28587.750000  \\n"\n'
        '        "50%                      18.500000                 28595.000000  \\n"\n'
        '        "75%                      25.750000                 28604.250000  \\n"\n'
        '        "max                      34.000000                 28613.000000  ")\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 10 code\n"
        '      ct_cell_outputs["display_data"] = df.describe()\n'
        "      # >>>>>>> End of Cell 10 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=10)\n"
        "\n"
        "  def test_00011(self, verbose=True):\n"
        '    """Test cell 11."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = (\n'
        '        "            geography geography_type                     year  \\\\\\n"\n'
        '        "count              32             32                       32   \\n"\n'
        '        "unique             32              3                        1   \\n"\n'
        '        "top     Half Moon Bay           City  2014-01-01T00:00:00.000   \\n"\n'
        '        "freq                1             15                       32   \\n"\n'
        '        "mean              NaN            NaN                      NaN   \\n"\n'
        '        "std               NaN            NaN                      NaN   \\n"\n'
        '        "min               NaN            NaN                      NaN   \\n"\n'
        '        "25%               NaN            NaN                      NaN   \\n"\n'
        '        "50%               NaN            NaN                      NaN   \\n"\n'
        '        "75%               NaN            NaN                      NaN   \\n"\n'
        '        "max               NaN            NaN                      NaN   \\n"\n'
        '        "\\n"\n'
        '        "        less_than_high_school_graduate  high_school_graduate  \\\\\\n"\n'
        '        "count                         32.00000             32.000000   \\n"\n'
        '        "unique                             NaN                   NaN   \\n"\n'
        '        "top                                NaN                   NaN   \\n"\n'
        '        "freq                               NaN                   NaN   \\n"\n'
        '        "mean                          17.80000              6.462500   \\n"\n'
        '        "std                           19.29944              4.693905   \\n"\n'
        '        "min                            0.00000              0.000000   \\n"\n'
        '        "25%                            6.82500              1.925000   \\n"\n'
        '        "50%                           13.90000              7.750000   \\n"\n'
        '        "75%                           20.97500              9.450000   \\n"\n'
        '        "max                          100.00000             16.400000   \\n"\n'
        '        "\\n"\n'
        '        "        some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\\\\n"\n'
        '        "count                            32.000000                    32.000000   \\n"\n'
        '        "unique                                 NaN                          NaN   \\n"\n'
        '        "top                                    NaN                          NaN   \\n"\n'
        '        "freq                                   NaN                          NaN   \\n"\n'
        '        "mean                              5.946875                     2.856250   \\n"\n'
        '        "std                               4.728430                     1.873919   \\n"\n'
        '        "min                               0.000000                     0.000000   \\n"\n'
        '        "25%                               2.525000                     2.100000   \\n"\n'
        '        "50%                               5.500000                     3.000000   \\n"\n'
        '        "75%                               8.800000                     3.600000   \\n"\n'
        '        "max                              18.500000                     9.100000   \\n"\n'
        '        "\\n"\n'
        '        "        :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \\n"\n'
        '        "count                     30.000000                    32.000000  \\n"\n'
        '        "unique                          NaN                          NaN  \\n"\n'
        '        "top                             NaN                          NaN  \\n"\n'
        '        "freq                            NaN                          NaN  \\n"\n'
        '        "mean                      17.733333                 25062.093750  \\n"\n'
        '        "std                        9.762466                  9502.711577  \\n"\n'
        '        "min                        1.000000                   312.000000  \\n"\n'
        '        "25%                        9.500000                 28587.750000  \\n"\n'
        '        "50%                       18.500000                 28595.000000  \\n"\n'
        '        "75%                       25.750000                 28604.250000  \\n"\n'
        '        "max                       34.000000                 28613.000000  ")\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 11 code\n"
        '      ct_cell_outputs["display_data"] = df.drop(\n'
        '          "location_1", axis=1).describe(include="all")\n'
        "      # >>>>>>> End of Cell 11 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=11)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00012(self, verbose=True):\n"
        '    """Test cell 12."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = (\n'
        '        "geography                              object\\n"\n'
        '        "geography_type                         object\\n"\n'
        '        "year                                   object\\n"\n'
        '        "less_than_high_school_graduate        float64\\n"\n'
        '        "high_school_graduate                  float64\\n"\n'
        '        "some_college_or_associate_s_degree    float64\\n"\n'
        '        "bachelor_s_degree_or_higher           float64\\n"\n'
        '        "location_1                             object\\n"\n'
        '        ":@computed_region_uph5_8hpn           float64\\n"\n'
        '        ":@computed_region_i2t2_cryp             int64\\n"\n'
        '        "dtype: object")\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 12 code\n"
        '      ct_cell_outputs["display_data"] = df.dtypes\n'
        "      # >>>>>>> End of Cell 12 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=12)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00013(self, verbose=True):\n"
        '    """Test cell 13."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = "2.85625"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 13 code\n"
        '      ct_cell_outputs["display_data"] = df.bachelor_s_degree_or_higher.mean()\n'
        "      # >>>>>>> End of Cell 13 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=13)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00014(self, verbose=True):\n"
        '    """Test cell 14."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = "32"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 14 code\n"
        '      ct_cell_outputs["display_data"] = df.geography.count()\n'
        "      # >>>>>>> End of Cell 14 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=14)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00015(self, verbose=True):\n"
        '    """Test cell 15."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        "    ct_saved_cell_outputs[\n"
        "        \"display_data\"] = \"array(['Town', 'City', 'CDP'], dtype=object)\"\n"
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 15 code\n"
        '      ct_cell_outputs["display_data"] = df.geography_type.unique()\n'
        "      # >>>>>>> End of Cell 15 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=15)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00016(self, verbose=True):\n"
        '    """Test cell 16."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = (\n'
        '        "0.0      4\\n"\n'
        '        "14.2     1\\n"\n'
        '        "8.5      1\\n"\n'
        '        "7.0      1\\n"\n'
        '        "100.0    1\\n"\n'
        '        "9.5      1\\n"\n'
        '        "11.9     1\\n"\n'
        '        "4.8      1\\n"\n'
        '        "31.1     1\\n"\n'
        '        "26.7     1\\n"\n'
        '        "6.2      1\\n"\n'
        '        "15.7     1\\n"\n'
        '        "22.1     1\\n"\n'
        '        "16.4     1\\n"\n'
        '        "6.3      1\\n"\n'
        '        "44.4     1\\n"\n'
        '        "20.9     1\\n"\n'
        '        "7.7      1\\n"\n'
        '        "9.2      1\\n"\n'
        '        "37.8     1\\n"\n'
        '        "3.3      1\\n"\n'
        '        "15.1     1\\n"\n'
        '        "48.1     1\\n"\n'
        '        "18.3     1\\n"\n'
        '        "21.2     1\\n"\n'
        '        "16.1     1\\n"\n'
        '        "13.6     1\\n"\n'
        '        "13.4     1\\n"\n'
        '        "20.1     1\\n"\n'
        '        "Name: less_than_high_school_graduate, dtype: int64")\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 16 code\n"
        "      ct_cell_outputs[\n"
        '          "display_data"] = df.less_than_high_school_graduate.value_counts()\n'
        "      # >>>>>>> End of Cell 16 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=16)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00018(self, verbose=True):\n"
        '    """Test cell 18."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        "    ct_saved_cell_outputs[\"display_data\"] = \"['a', '', '', '...', '', 'b']\"\n"
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 18 code\n"
        '      ct_cell_outputs["display_data"] = "a   ...  b".split(" ")\n'
        "      # >>>>>>> End of Cell 18 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=18)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00019(self, verbose=True):\n"
        '    """Test cell 19."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = (\n'
        '        \'<>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?\\n\'\n'
        '        \'<>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?\\n\'\n'
        '        \'<ipython-input-38-7e9601f26686>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?\\n\'\n'
        '        "  \\"\\" is \'\'\\n")\n'
        '    ct_saved_cell_outputs["display_data"] = "True"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 19 code\n"
        '      ct_cell_outputs["display_data"] = "" is ""\n'
        "      # >>>>>>> End of Cell 19 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=19)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00020(self, verbose=True):\n"
        '    """Test cell 20."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = "\'    \'"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 20 code\n"
        '      ct_cell_outputs["display_data"] = " " * 4\n'
        "      # >>>>>>> End of Cell 20 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=20)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00021(self, verbose=True):\n"
        '    """Test cell 21."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = None\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 21 code\n"
        '      ct_cell_outputs["display_data"] = None\n'
        "      # >>>>>>> End of Cell 21 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=21)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00022(self, verbose=True):\n"
        '    """Test cell 22."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = "\'True\'"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 22 code\n"
        '      ct_cell_outputs["display_data"] = str(True)\n'
        "      # >>>>>>> End of Cell 22 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=22)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "  def test_00023(self, verbose=True):\n"
        '    """Test cell 23."""\n'
        "    ct_cell_outputs = defaultdict(lambda: None)\n"
        "\n"
        "    ct_saved_cell_outputs = defaultdict(lambda: None)\n"
        '    ct_saved_cell_outputs["stdout"] = None\n'
        '    ct_saved_cell_outputs["stderr"] = None\n'
        '    ct_saved_cell_outputs["display_data"] = "True"\n'
        "\n"
        '    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (\n'
        "        io.StringIO(),\n"
        "        io.StringIO(),\n"
        "    )\n"
        '    capture_log(root_logger, ct_cell_outputs["stderr"])\n'
        '    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(\n'
        '        ct_cell_outputs["stderr"]):\n'
        "\n"
        "      # <<<<<<< Cell 23 code\n"
        '      ct_cell_outputs["display_data"] = """True""" == str(True)\n'
        "      # >>>>>>> End of Cell 23 code\n"
        "\n"
        "    ct_cell_outputs, ct_saved_cell_outputs = postprocess(\n"
        "        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=23)\n"
        "\n"
        '    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])\n'
        "\n"
        '    self.assertEqual(ct_cell_outputs["display_data"],\n'
        '                     ct_saved_cell_outputs["display_data"])\n'
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "  main()\n"
        "\n")
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 20 code
      ct_cell_outputs["display_data"] = print(
          cellconvert.make_tests(
              callbacks=["black", "yapf"],
              update=False,
              insert_saved_outputs=True))
      # >>>>>>> End of Cell 20 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=20)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00021(self, verbose=True):
    """Just test assert"""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 21 code
      ct_cell_outputs["display_data"] = self.assertTrue(1 == 1)
      # >>>>>>> End of Cell 21 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=21)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])


if __name__ == "__main__":
  main()
