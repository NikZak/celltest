"""Template file for celltest.

Should contain only a dictionary in python format
"""
{  #  pylint: disable=pointless-statement
    "100 head if header given": {
        "source": '''\
{}
''',
        "replacements": ["header_file",],
        "control": {
            "if_head_level": ["header_file"]
        },
    },
    "100 head": {
        "source":
            '''\
"""Tests automatically generated from notebook {}.

Do not make direct changes in this file as it may be
regenerated, make all changes in the notebook.

Accepted parameters in notebook cells to control test flow:
{}

Accepted callbacks (if installed) to prettify the .py test file:
{}

To change the test file default copy and change the template.py from
celltest/src/celltest.
"""
''',
        "replacements": [
            "notebook_name",
            "accepted_params",
            "accepted_callbacks",
        ],
        "control": {
            "if_head_level": ["not header_file"]
        },
    },
    "200 imports_head": {
        "source":
            '''\
from collections import defaultdict
import io
import logging
from contextlib import redirect_stdout, redirect_stderr
from unittest import TestCase, main
'''
    },
    "210 imports_body": {
        "source": '''\
{}
''',
        "replacements": ["imports",],
    },
    "220 insert_celltest_funcs": {
        "source": '''\

{}
''',
        "replacements": ["funclib",],
    },
    "300 setup": {
        "source":
            '''\

root_logger = logging.getLogger()
if not root_logger.handlers:
    logging.basicConfig()
''',
    },
    "310 setup": {
        "source": '''\

TestCase.maxDiff = None
{}
''',
        "replacements": ["setup",],
    },
    "400 class_head": {
        "source": '''\

class Test(TestCase):
    """Test class."""
''',
    },
    "410 class_head_if_not_insert": {
        "source":
            '''\

    def __init__(self, *args, **kwargs):
        """Init method."""
        super().__init__(*args, **kwargs)
        self.ct_saved_cell_outputs = get_outputs(
            "{}")
''',
        "replacements": ["filefullpath",],
        "control": {
            "if_head_level": ["not insert_saved_outputs"]
        },
    },
    "500 test": {
        "source": {
            "500 test_head": {
                "source": '''\

    def test_{}(self, verbose=True):
''',
                "replacements": ["index_iter_name"],
            },
            "501 test_head if not comment": {
                "source":
                    '''\
        """Test cell {}."""
        ct_cell_outputs = defaultdict(lambda: None)
''',
                "replacements": ["index_iter"],
                "control": {
                    "if_cell_level": ["not comment"]
                }
            },
            "501 test_head if comment": {
                "source":
                    '''\
        """{}"""
        ct_cell_outputs = defaultdict(lambda: None)
''',
                "replacements": ["comment"],
                "control": {
                    "if_cell_level": ["comment"]
                }
            },
            "502 test_head_if_insert_outputs": {
                "source":
                    '''\

        ct_saved_cell_outputs = defaultdict(lambda :None)
        ct_saved_cell_outputs["stdout"] = {}
        ct_saved_cell_outputs["stderr"] = {}
        ct_saved_cell_outputs["display_data"] = {}
''',
                "replacements": [
                    "ct_saved_cell_outputs_stdout",
                    "ct_saved_cell_outputs_stderr",
                    "ct_saved_cell_outputs_display_data"
                ],
                "control": {
                    "if_head_level": ["insert_saved_outputs"]
                },
            },
            "502 test_head_if_not_insert_outputs": {
                "source":
                    '''\

        ct_saved_cell_outputs = self.ct_saved_cell_outputs[{}]
''',
                "replacements": ["index_iter"],
                "control": {
                    "if_head_level": ["not insert_saved_outputs"]
                },
            },
            "503 test_head": {
                "source":
                    '''\

        ct_cell_outputs["stdout"], ct_cell_outputs["stderr"] = io.StringIO(), io.StringIO(
        )
        capture_log(root_logger, ct_cell_outputs["stderr"])
        with redirect_stdout(ct_cell_outputs["stdout"]), redirect_stderr(
            ct_cell_outputs["stderr"]):
''',
                "replacements": ["index_iter_name", "index_iter", "index_iter"],
            },
            "504 test_all_previous": {
                "source":
                    '''\
            # run all previous cells to initiate class internal state
''',
                "control": {
                    "if_cell_level": ["run_all_till_now"],
                }
            },
            "505 test_all_previous": {
                "source": '''\
{}
''',
                "replacements": ["run_all_till_now"],
                "indent": 3,
                "control": {
                    "if_cell_level": ["run_all_till_now"]
                }
            },
            "511 test_body": {
                "source": '''\

# <<<<<<< Cell {} code
''',
                "replacements": ["index_iter"],
                "indent": 3,
            },
            "515 test_body": {
                "source": '''\
{}
''',
                "replacements": ["value_iter"],
                "callbacks": ["replace_asserts", "save_outputs"],
                "indent": 3,
            },
            "519 test_body": {
                "source": '''\
# >>>>>>> End of Cell {} code
''',
                "replacements": ["index_iter"],
                "indent": 3,
            },
            "520 test_tail": {
                "source":
                    '''\

        ct_cell_outputs, ct_saved_cell_outputs = postprocess(
            ct_cell_outputs, ct_saved_cell_outputs, verbose=verbose, cell_n={})
''',
                "replacements": ["index_iter"],
            },
            "530 test_tail_stdout": {
                "source":
                    '''\

        self.assertEqual(ct_cell_outputs["stdout"], ct_saved_cell_outputs["stdout"])
''',
                "replacements": ["index_iter"],
                "control": {
                    "if_cell_level": [
                        "not ignore_outputs", "not ignore_stdout"
                    ],
                }
            },
            "540 test_tail_stderr": {
                "source":
                    '''\

        self.assertEqual(ct_cell_outputs["stderr"], ct_saved_cell_outputs["stderr"])
''',
                "replacements": ["index_iter"],
                "control": {
                    "if_cell_level": [
                        "not ignore_outputs", "not ignore_stderr"
                    ],
                }
            },
            "550 test_tail_outputs": {
                "source":
                    '''\

        self.assertEqual(ct_cell_outputs["display_data"],
                           ct_saved_cell_outputs["display_data"])
''',
                "replacements": ["index_iter"],
                "control": {
                    "if_cell_level": [
                        "not ignore_outputs", "not ignore_display_data"
                    ],
                }
            },
        },
        "control": {
            "loop": "code_d_"
        }
    },
    "600 tail": {
        "source": '''\

if __name__ == '__main__':
    main()
'''
    }
}
