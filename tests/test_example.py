"""Tests automatically generated from notebook example.ipynb.

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
import tokenize
from collections import defaultdict
from contextlib import redirect_stderr, redirect_stdout
from unittest import TestCase, main

import matplotlib
import pandas as pd
from IPython.core.formatters import DisplayFormatter


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
df = pd.read_json("https://data.smcgov.org/resource/mb6a-xn89.json")
logging.error("test")
logging.error("test")
print("test")
logging.error("test")
print("test")


class Test(TestCase):
  """Test class."""

  def test_00006(self, verbose=True):
    """Test cell 6."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = "Hello World\n" "Hello World\n" "test\n"
    ct_saved_cell_outputs["stderr"] = ("ERROR:root:test\n"
                                       "ERROR:root:test\n"
                                       "ERROR:root:test\n")
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 6 code
      print("Hello World")
      print("Hello World")
      logging.error("test")
      logging.error("test")
      print("test")
      ct_cell_outputs["display_data"] = logging.error("test")
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
    ct_saved_cell_outputs["stdout"] = "Hello World\n"
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = None

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 7 code
      ct_cell_outputs["display_data"] = print("Hello World")
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
        "        geography geography_type                     year  \\\n"
        "0        Atherton           Town  2014-01-01T00:00:00.000   \n"
        "1           Colma           Town  2014-01-01T00:00:00.000   \n"
        "2     Foster City           City  2014-01-01T00:00:00.000   \n"
        "3  Portola Valley           Town  2014-01-01T00:00:00.000   \n"
        "4    Redwood City           City  2014-01-01T00:00:00.000   \n"
        "\n"
        "   less_than_high_school_graduate  high_school_graduate  \\\n"
        "0                            13.6                  12.3   \n"
        "1                             6.3                   6.4   \n"
        "2                            11.9                   9.7   \n"
        "3                            48.1                   0.0   \n"
        "4                            16.4                  10.6   \n"
        "\n"
        "   some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\n"
        "0                                 2.7                          3.5   \n"
        "1                                10.4                          2.4   \n"
        "2                                 2.0                          2.9   \n"
        "3                                 0.0                          1.8   \n"
        "4                                 6.6                          3.0   \n"
        "\n"
        "                                          location_1  \\\n"
        "0  {'type': 'Point', 'coordinates': [-122.2, 37.4...   \n"
        "1  {'type': 'Point', 'coordinates': [-122.455556,...   \n"
        "2  {'type': 'Point', 'coordinates': [-122.266389,...   \n"
        "3  {'type': 'Point', 'coordinates': [-122.218611,...   \n"
        "4  {'type': 'Point', 'coordinates': [-122.236111,...   \n"
        "\n"
        "   :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \n"
        "0                          2.0                        28596  \n"
        "1                          4.0                        28588  \n"
        "2                          6.0                          319  \n"
        "3                         14.0                        28597  \n"
        "4                         21.0                        28607  ")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 8 code
      ct_cell_outputs["display_data"] = df.head(5)
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
    ct_saved_cell_outputs["display_data"] = "(32, 10)"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 9 code
      ct_cell_outputs["display_data"] = df.shape
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
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "       less_than_high_school_graduate  high_school_graduate  \\\n"
        "count                        32.00000             32.000000   \n"
        "mean                         17.80000              6.462500   \n"
        "std                          19.29944              4.693905   \n"
        "min                           0.00000              0.000000   \n"
        "25%                           6.82500              1.925000   \n"
        "50%                          13.90000              7.750000   \n"
        "75%                          20.97500              9.450000   \n"
        "max                         100.00000             16.400000   \n"
        "\n"
        "       some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\n"
        "count                           32.000000                    32.000000   \n"
        "mean                             5.946875                     2.856250   \n"
        "std                              4.728430                     1.873919   \n"
        "min                              0.000000                     0.000000   \n"
        "25%                              2.525000                     2.100000   \n"
        "50%                              5.500000                     3.000000   \n"
        "75%                              8.800000                     3.600000   \n"
        "max                             18.500000                     9.100000   \n"
        "\n"
        "       :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \n"
        "count                    30.000000                    32.000000  \n"
        "mean                     17.733333                 25062.093750  \n"
        "std                       9.762466                  9502.711577  \n"
        "min                       1.000000                   312.000000  \n"
        "25%                       9.500000                 28587.750000  \n"
        "50%                      18.500000                 28595.000000  \n"
        "75%                      25.750000                 28604.250000  \n"
        "max                      34.000000                 28613.000000  ")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 10 code
      ct_cell_outputs["display_data"] = df.describe()
      # >>>>>>> End of Cell 10 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=10)

  def test_00011(self, verbose=True):
    """Test cell 11."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = (
        "       geography geography_type                     year  \\\n"
        "count         32             32                       32   \n"
        "unique        32              3                        1   \n"
        "top     Woodside           City  2014-01-01T00:00:00.000   \n"
        "freq           1             15                       32   \n"
        "mean         NaN            NaN                      NaN   \n"
        "std          NaN            NaN                      NaN   \n"
        "min          NaN            NaN                      NaN   \n"
        "25%          NaN            NaN                      NaN   \n"
        "50%          NaN            NaN                      NaN   \n"
        "75%          NaN            NaN                      NaN   \n"
        "max          NaN            NaN                      NaN   \n"
        "\n"
        "        less_than_high_school_graduate  high_school_graduate  \\\n"
        "count                         32.00000             32.000000   \n"
        "unique                             NaN                   NaN   \n"
        "top                                NaN                   NaN   \n"
        "freq                               NaN                   NaN   \n"
        "mean                          17.80000              6.462500   \n"
        "std                           19.29944              4.693905   \n"
        "min                            0.00000              0.000000   \n"
        "25%                            6.82500              1.925000   \n"
        "50%                           13.90000              7.750000   \n"
        "75%                           20.97500              9.450000   \n"
        "max                          100.00000             16.400000   \n"
        "\n"
        "        some_college_or_associate_s_degree  bachelor_s_degree_or_higher  \\\n"
        "count                            32.000000                    32.000000   \n"
        "unique                                 NaN                          NaN   \n"
        "top                                    NaN                          NaN   \n"
        "freq                                   NaN                          NaN   \n"
        "mean                              5.946875                     2.856250   \n"
        "std                               4.728430                     1.873919   \n"
        "min                               0.000000                     0.000000   \n"
        "25%                               2.525000                     2.100000   \n"
        "50%                               5.500000                     3.000000   \n"
        "75%                               8.800000                     3.600000   \n"
        "max                              18.500000                     9.100000   \n"
        "\n"
        "        :@computed_region_uph5_8hpn  :@computed_region_i2t2_cryp  \n"
        "count                     30.000000                    32.000000  \n"
        "unique                          NaN                          NaN  \n"
        "top                             NaN                          NaN  \n"
        "freq                            NaN                          NaN  \n"
        "mean                      17.733333                 25062.093750  \n"
        "std                        9.762466                  9502.711577  \n"
        "min                        1.000000                   312.000000  \n"
        "25%                        9.500000                 28587.750000  \n"
        "50%                       18.500000                 28595.000000  \n"
        "75%                       25.750000                 28604.250000  \n"
        "max                       34.000000                 28613.000000  ")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 11 code
      ct_cell_outputs["display_data"] = df.drop(
          "location_1", axis=1).describe(include="all")
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
        "geography                              object\n"
        "geography_type                         object\n"
        "year                                   object\n"
        "less_than_high_school_graduate        float64\n"
        "high_school_graduate                  float64\n"
        "some_college_or_associate_s_degree    float64\n"
        "bachelor_s_degree_or_higher           float64\n"
        "location_1                             object\n"
        ":@computed_region_uph5_8hpn           float64\n"
        ":@computed_region_i2t2_cryp             int64\n"
        "dtype: object")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 12 code
      ct_cell_outputs["display_data"] = df.dtypes
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
    ct_saved_cell_outputs["display_data"] = "2.85625"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 13 code
      ct_cell_outputs["display_data"] = df.bachelor_s_degree_or_higher.mean()
      # >>>>>>> End of Cell 13 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=13)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00014(self, verbose=True):
    """Test cell 14."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = "32"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 14 code
      ct_cell_outputs["display_data"] = df.geography.count()
      # >>>>>>> End of Cell 14 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=14)

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
        "display_data"] = "array(['Town', 'City', 'CDP'], dtype=object)"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 15 code
      ct_cell_outputs["display_data"] = df.geography_type.unique()
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
        "0.0      4\n"
        "14.2     1\n"
        "8.5      1\n"
        "7.0      1\n"
        "100.0    1\n"
        "9.5      1\n"
        "11.9     1\n"
        "4.8      1\n"
        "31.1     1\n"
        "26.7     1\n"
        "6.2      1\n"
        "15.7     1\n"
        "22.1     1\n"
        "16.4     1\n"
        "6.3      1\n"
        "44.4     1\n"
        "20.9     1\n"
        "7.7      1\n"
        "9.2      1\n"
        "37.8     1\n"
        "3.3      1\n"
        "15.1     1\n"
        "48.1     1\n"
        "18.3     1\n"
        "21.2     1\n"
        "16.1     1\n"
        "13.6     1\n"
        "13.4     1\n"
        "20.1     1\n"
        "Name: less_than_high_school_graduate, dtype: int64")

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 16 code
      ct_cell_outputs[
          "display_data"] = df.less_than_high_school_graduate.value_counts()
      # >>>>>>> End of Cell 16 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=16)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00018(self, verbose=True):
    """Test cell 18."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = "['a', '', '', '...', '', 'b']"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 18 code
      ct_cell_outputs["display_data"] = "a   ...  b".split(" ")
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
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = (
        '<>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?\n'
        '<>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?\n'
        '<ipython-input-17-7e9601f26686>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?\n'
        "  \"\" is ''\n")
    ct_saved_cell_outputs["display_data"] = "True"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 19 code
      ct_cell_outputs["display_data"] = "" is ""
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
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = "'    '"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 20 code
      ct_cell_outputs["display_data"] = " " * 4
      # >>>>>>> End of Cell 20 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=20)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00021(self, verbose=True):
    """Test cell 21."""
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
      ct_cell_outputs["display_data"] = None
      # >>>>>>> End of Cell 21 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=21)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00022(self, verbose=True):
    """Test cell 22."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = "'True'"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 22 code
      ct_cell_outputs["display_data"] = str(True)
      # >>>>>>> End of Cell 22 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=22)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])

  def test_00023(self, verbose=True):
    """Test cell 23."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = defaultdict(lambda: None)
    ct_saved_cell_outputs["stdout"] = None
    ct_saved_cell_outputs["stderr"] = None
    ct_saved_cell_outputs["display_data"] = "True"

    ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = (
        io.StringIO(),
        io.StringIO(),
    )
    capture_log(root_logger, ct_cell_outputs["stderr"])
    with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
        ct_cell_outputs["stderr"]):

      # <<<<<<< Cell 23 code
      ct_cell_outputs["display_data"] = """True""" == str(True)
      # >>>>>>> End of Cell 23 code

    ct_cell_outputs, ct_saved_cell_outputs = postprocess(
        ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n=23)

    self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])

    self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])

    self.assertEqual(ct_cell_outputs["display_data"],
                     ct_saved_cell_outputs["display_data"])


if __name__ == "__main__":
  main()
