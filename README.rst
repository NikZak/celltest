========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/celltest/badge/?style=flat
    :target: https://readthedocs.org/projects/celltest
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/NikZak/celltest.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/NikZak/celltest

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/NikZak/celltest?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/NikZak/celltest

.. |requires| image:: https://requires.io/github/NikZak/celltest/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/NikZak/celltest/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/NikZak/celltest/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/NikZak/celltest

.. |version| image:: https://img.shields.io/pypi/v/celltest.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/celltest

.. |wheel| image:: https://img.shields.io/pypi/wheel/celltest.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/celltest

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/celltest.svg
    :alt: Supported versions
    :target: https://pypi.org/project/celltest

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/celltest.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/celltest

.. |commits-since| image:: https://img.shields.io/github/commits-since/NikZak/celltest/v0.0.2.svg
    :alt: Commits since latest release
    :target: https://github.com/NikZak/celltest/compare/v0.0.2...master



.. end-badges

Use jupyter notebook or jupyter lab in the testing process. This software converts notebook cells to unittests compatible with pytest, coverage, tox.

Installation
============

::

    pip install celltest

You can also install the in-development version with::

    pip install https://github.com/NikZak/celltest/archive/master.zip


Usage
=====

From command line

::

    celltest [-h] -f FILES [FILES ...] [-c CALLBACKS [CALLBACKS ...]] [-nio] [-o [OUTPUT]] [-st [STANDARD_TEMPLATE]] [-ct [CUSTOM_TEMPLATE]] [-hf [HEADER]] [-v]

Optional arguments::

  -h, --help            show help message and exit

  -f FILES [FILES ...], --files FILES [FILES ...]
                        <Required> notebook file(s) to convert

  -c CALLBACKS [CALLBACKS ...], --callbacks CALLBACKS [CALLBACKS ...]
                        callbacks to call after the test file creation (e.g. isort, black, yapf)

  -nio, --not_insert_outputs
                        do not insert cell ouputs in the test file (then outputs are read from notebook during testing)

  -o [OUTPUT], --output [OUTPUT]
                        output file. Defaults to test_[notebook name].py

  -st [STANDARD_TEMPLATE], --standard_template [STANDARD_TEMPLATE]
                        standard template file: 1: default template 2: minimalistic template without checking outputs

  -ct [CUSTOM_TEMPLATE], --custom_template [CUSTOM_TEMPLATE]
                        custom template file

  -hf [HEADER], --header [HEADER]
                        header file. Header to insert in every test file

  -v, --verbose         increase output verbosity

From notebook cell

::

    # CT: ignore
    # convert current notebook to unittest
    from celltest.cells import CellConvert
    CellConvert(callbacks=['isort', 'black', 'yapf']).run()

Accepted parameters to control test flow::

    'comment', 'setup', 'ignore_outputs', 'ignore_stderr', 'ignore_stdout', 'ignore', 'ignore_display_data', 'run_all_till_now'

Parameters can be either specified in first line (after the % magic) of the notebook cells (e.g.)::

    # CT: ignore_outputs comment "Test ABC method"

or written in cell metadata:

::

    { "celltest :
        ["ignore_outputs", "comment", "Test ABC method"]
    }

In case of conflicts line parameters are prioritised

Accepted callbacks (if installed) to prettify the .py test file::

    isort, black, yapf

Documentation
=============


https://celltest.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
