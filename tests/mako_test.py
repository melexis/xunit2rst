#!/usr/bin/env python3
''' Test suite for error handling for Mako template '''
import unittest
from pathlib import Path
from unittest import TestCase

from mlx.xunit2rst import ITEST, render_template

TEST_OUT_DIR = Path(__file__).parent / 'test_out'


class TestMako(unittest.TestCase):

    def test_mako_error_handling(self):
        ''' Tests error logging and re-raising of an Exception in Mako template by intentionally not passing a
        variable '''
        kwargs = {
            'report_name': 'my_report',
            'info': ITEST,
            'prefix': 'MAKO_TEST-',
        }
        test_case = TestCase()
        with test_case.assertLogs() as log_cm:
            with self.assertRaises(TypeError):
                render_template((TEST_OUT_DIR / 'never_created_file.rst'), **kwargs)
        test_case.assertIn('Exception raised in Mako template, which will be re-raised after logging line info:',
                           log_cm.output[0])
        test_case.assertIn('File ', log_cm.output[-1])
        test_case.assertIn('line ', log_cm.output[-1])
        test_case.assertIn("in render_body: '% for suite_idx, suite in enumerate(test_suites):'",
                           log_cm.output[-1])


if __name__ == '__main__':
    unittest.main()
