"""Tests automatically generated from notebook example.ipynb.

Do not make direct changes in this file as it may be
regenerated, make all changes in the notebook.

Accepted parameters in notebook cells to control test flow:
['setup', 'ignore_outputs', 'ignore_stderr', 'ignore_stdout', 'ignore', 'ignore_display_data', 'run_all']

Accepted callbacks (if installed) to prettify the .py test file:
['black', 'yapf']

To change the test file default copy and change the template.py from
celltest/src/celltest.
"""
from collections import defaultdict
import io
from contextlib import redirect_stdout, redirect_stderr
from unittest import TestCase, main
from celltest.funclib import get_outputs, capture_log, postprocess
import pandas as pd
import tokenize, io
import os
import matplotlib
import logging

TestCase.maxDiff = None
root_logger = logging.getLogger()
if not root_logger.handlers:
  logging.basicConfig()
df = pd.read_json("https://data.smcgov.org/resource/mb6a-xn89.json")
logging.error("test")
logging.error("test")
print("test")
logging.error("test")
print("test")


class Test(TestCase):
  """Test class."""

  def __init__(self, *args, **kwargs):
    """Init method."""
    super().__init__(*args, **kwargs)
    self.ct_saved_cell_outputs = get_outputs(
        "/home/nikolay/Projects/source/celltest/tests/example.ipynb")

  def test_cell_00006(self, verbose=True, skip_mode=False):
    """Test cell 6."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[6]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00007(self, verbose=True, skip_mode=False):
    """Test cell 7."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[7]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00008(self, verbose=True, skip_mode=False):
    """Test cell 8."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[8]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00009(self, verbose=True, skip_mode=False):
    """Test cell 9."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[9]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00010(self, verbose=True, skip_mode=False):
    """Test cell 10."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[10]

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

  def test_cell_00011(self, verbose=True, skip_mode=False):
    """Test cell 11."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[11]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00012(self, verbose=True, skip_mode=False):
    """Test cell 12."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[12]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00013(self, verbose=True, skip_mode=False):
    """Test cell 13."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[13]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00014(self, verbose=True, skip_mode=False):
    """Test cell 14."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[14]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00015(self, verbose=True, skip_mode=False):
    """Test cell 15."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[15]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00016(self, verbose=True, skip_mode=False):
    """Test cell 16."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[16]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00018(self, verbose=True, skip_mode=False):
    """Test cell 18."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[18]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00019(self, verbose=True, skip_mode=False):
    """Test cell 19."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[19]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00020(self, verbose=True, skip_mode=False):
    """Test cell 20."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[20]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00021(self, verbose=True, skip_mode=False):
    """Test cell 21."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[21]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00022(self, verbose=True, skip_mode=False):
    """Test cell 22."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[22]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])

  def test_cell_00023(self, verbose=True, skip_mode=False):
    """Test cell 23."""
    ct_cell_outputs = defaultdict(lambda: None)

    ct_saved_cell_outputs = self.ct_saved_cell_outputs[23]

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

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stdout"],
                       ct_saved_cell_outputs["stdout"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["stderr"],
                       ct_saved_cell_outputs["stderr"])

    if not skip_mode:
      self.assertEqual(ct_cell_outputs["display_data"],
                       ct_saved_cell_outputs["display_data"])


if __name__ == "__main__":
  main()
