#!/usr/bin/env python3
''' Test suite for error handling for Mako template '''
from unittest import TestCase
from pathlib import Path
from nose.tools import assert_raises
from mlx.xunit2rst import render_template, ITEST

TEST_OUT_DIR = Path(__file__).parent / 'test_out'


def test_mako_error_handling():
    ''' Tests error logging and re-raising of an Exception in Mako template by intentionally not passing a variable '''
    kwargs = {
        'report_name': 'my_report',
        'info': ITEST,
        'prefix': 'MAKO_TEST-',
    }
    test_case = TestCase()
    with test_case.assertLogs() as log_cm:
        with assert_raises(TypeError):
            render_template((TEST_OUT_DIR / 'never_created_file.rst'), **kwargs)
    test_case.assertIn('Exception raised in Mako template, which will be re-raised after logging line info:',
                       log_cm.output[0])
    test_case.assertIn('File ', log_cm.output[-1])
    test_case.assertIn('line ', log_cm.output[-1])
    test_case.assertIn("in render_body: '% for suite in test_suites:'", log_cm.output[-1])
