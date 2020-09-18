"""Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcelltest` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``celltest.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``celltest.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import os
import logging
import argparse
from celltest import cells


def main():
  """Convert notebooks to unitests."""
  parser = argparse.ArgumentParser(description='Convert notebooks to unittests')
  parser.add_argument(
      '-f',
      '--files',
      nargs='+',
      help='<Required> notebook file(s) to convert',
      required=True)
  parser.add_argument(
      '-c',
      '--callbacks',
      nargs='+',
      help='callbacks to call after the test file creation (e.g. isort, black, yapf)',
      default=[],
      required=False)
  parser.add_argument(
      "-nio",
      "--not_insert_outputs",
      help="do not insert cell ouputs in the test file (then outputs are "
      "read from notebook during testing)",
      action="store_true",
      default=False)
  parser.add_argument(
      "-o",
      "--output",
      nargs='?',
      help="output file. Defaults to test_[notebook name].py")
  parser.add_argument(
      "-st",
      "--standard_template",
      nargs='?',
      help="standard template file: \n"
      "    1: default template\n"
      "    2: minimalistic template without checking outputs",
      default=None)
  parser.add_argument(
      "-ct",
      "--custom_template",
      nargs='?',
      help="custom template file",
      default=None)
  parser.add_argument(
      "-hf",
      "--header",
      nargs='?',
      help="header file. Header to insert in every test file",
      default=None)
  parser.add_argument(
      "-v", "--verbose", help="increase output verbosity", action="store_true")

  args = parser.parse_args()
  for index, file_name in enumerate(args.files):
    if args.output:
      output_file = args.output + "" if len(
          args.files) == 1 else "_" + str(index)
    else:
      output_file = None
    if not os.path.isfile(file_name):
      logging.error("invalid file name %s:", file_name)
      continue
    try:
      cellconvert = cells.CellConvert(
          filepath=file_name,
          standard_template=args.standard_template,
          custom_template=args.custom_template,
          callbacks=args.callbacks,
          insert_saved_outputs=not args.not_insert_outputs,
          output_file=output_file,
          header_file=args.header,
          verbose=args.verbose,
      )
      cellconvert.run()
      del cellconvert
    except Exception as excp:
      raise excp

  return 0
