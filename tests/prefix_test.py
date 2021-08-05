#!/usr/bin/env python3
''' Test suite for functions that set the prefix and prefix_set variables '''
from pathlib import Path

import nose
from nose.tools import assert_equal, assert_not_equal, assert_raises

from mlx.xunit2rst import build_prefix_and_set, parse_xunit_root, verify_prefix_set, ITEST, UTEST, QTEST

TEST_IN_DIR = Path(__file__).parent / 'test_in'


def test_build_prefix_and_set_utest_default():
    ''' Use default prefix for unit test reports '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_no_prefix_report.xml')
    assert_equal(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
    assert_equal(prefix_set, initial_prefix_set)
    assert_equal(prefix, 'UTEST-')


def test_build_prefix_and_set_itest_default():
    ''' Use default prefix for integration test reports '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
    assert_equal(initial_prefix_set, ITEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
    assert_equal(prefix_set, initial_prefix_set)
    assert_equal(prefix, 'ITEST-')


def test_build_prefix_and_set_from_name():
    ''' Get prefix from element name '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
    assert_equal(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
    assert_equal(prefix_set, initial_prefix_set)
    assert_equal(prefix, 'UTEST_MY_LIB-')


def test_build_prefix_and_set_from_arg():
    ''' Get prefix from input argument `--prefix` and trim suffix of prefix '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
    assert_equal(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, 'TEST_MY_LIB_-', True, None)
    assert_equal(prefix_set, initial_prefix_set)
    assert_equal(prefix, 'TEST_MY_LIB-')


def test_build_prefix_and_set_from_arg_swap_set():
    '''
    Get prefix from input argument `--prefix` and base prefix_set on its first letter.
    Don't trim suffix of prefix.
    '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
    assert_equal(initial_prefix_set, ITEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, 'UTEST_MY_LIB_-', False, None)
    assert_not_equal(prefix_set, initial_prefix_set)
    assert_equal(prefix_set, UTEST)
    assert_equal(prefix, 'UTEST_MY_LIB_-')


def test_build_prefix_and_set_priority():
    ''' Argument --type must have the highest priority for determining the correct prefix_set. '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
    assert_equal(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, 'UTEST_HOWDY-', False, 'i')
    assert_not_equal(prefix_set, initial_prefix_set)
    assert_equal(prefix_set, ITEST)
    assert_equal(prefix, 'UTEST_HOWDY-')


def test_verify_prefix_set():
    '''
    Tests verify_prefix_set function. The --type argument should have the highest priority and must
    start with u/i/q (case-insensitive). The prefix argument has the second highest priority. A last resort is to
    keep the input prefix_set.
    '''
    assert_equal(verify_prefix_set(UTEST, 'UTEST-', 'Itest'), ITEST)
    assert_equal(verify_prefix_set(UTEST, 'UTEST-', 'i'), ITEST)
    assert_equal(verify_prefix_set(UTEST, '', 'i'), ITEST)
    assert_equal(verify_prefix_set(ITEST, 'ITEST-', 'Utest'), UTEST)
    assert_equal(verify_prefix_set(UTEST, 'ITEST-', 'u'), UTEST)
    assert_equal(verify_prefix_set(UTEST, 'UTEST-', 'u'), UTEST)
    assert_equal(verify_prefix_set(UTEST, 'BLAH-', None), UTEST)
    assert_equal(verify_prefix_set(ITEST, 'BLAH-', None), ITEST)
    assert_equal(verify_prefix_set(UTEST, 'ITEST-', None), ITEST)
    assert_equal(verify_prefix_set(ITEST, 'UTEST-', None), UTEST)
    assert_equal(verify_prefix_set(ITEST, 'QTEST-', None), QTEST)
    assert_equal(verify_prefix_set(ITEST, 'ITEST-', 'q'), QTEST)
    assert_equal(verify_prefix_set(UTEST, 'UTEST-', 'Qtest'), QTEST)
    assert_equal(verify_prefix_set(QTEST, '', 'u'), UTEST)
    assert_equal(verify_prefix_set(QTEST, '', 'i'), ITEST)
    assert_equal(verify_prefix_set(QTEST, 'UTEST', 'i'), ITEST)
    assert_equal(verify_prefix_set(QTEST, 'FOO-', None), QTEST)
    with assert_raises(ValueError):
        verify_prefix_set(UTEST, 'UTEST-', 't')
    with assert_raises(ValueError):
        verify_prefix_set(ITEST, 'ITEST', 't')
    with assert_raises(ValueError):
        verify_prefix_set(ITEST, '', '')
    with assert_raises(ValueError):
        verify_prefix_set(QTEST, '', 't')


if __name__ == '__main__':
    nose.main()
