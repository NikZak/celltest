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
    "200 imports_head": {
        "source":
            '''\
from collections import defaultdict
import io
import logging
from unittest import TestCase, main
'''
    },
    "210 imports_body": {
        "source": '''\
{}
''',
        "replacements": ["imports",],
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
    "500 test": {
        "source": {
            "500 test_head": {
                "source": '''\

    def test_{}(self, verbose=True):
''',
                "replacements": ["index_iter_name"],
            },
            "501 test_head if not comment": {
                "source": '''\
        """Test cell {}."""
''',
                "replacements": ["index_iter"],
                "control": {
                    "if_cell_level": ["not comment"]
                }
            },
            "501 test_head if comment": {
                "source": '''\
        """{}"""
''',
                "replacements": ["comment"],
                "control": {
                    "if_cell_level": ["comment"]
                }
            },
            "505 test_all_previous": {
                "source": '''\
{}
''',
                "replacements": ["run_all_till_now"],
                "indent": 2,
                "control": {
                    "if_cell_level": ["run_all_till_now"]
                }
            },
            "515 test_body": {
                "source": '''\
{}
''',
                "replacements": ["value_iter"],
                "callbacks": ["replace_asserts"],
                "indent": 2,
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
