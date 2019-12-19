from pathlib import Path

import nose
from nose.tools import assert_equals, assert_not_equals, assert_raises

from mlx.xunit2rst import build_prefix_and_set, parse_xunit_root, verify_prefix_set, ITEST, UTEST

TEST_IN_DIR = Path(__file__).parent / 'test_in'


def build_prefix_and_set_utest_default_test():
    ''' Use default prefix for unit test reports '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_no_prefix_report.xml')
    assert_equals(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
    assert_equals(prefix_set, initial_prefix_set)
    assert_equals(prefix, 'UTEST-')


def build_prefix_and_set_itest_default_test():
    ''' Use default prefix for integration test reports '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
    assert_equals(initial_prefix_set, ITEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
    assert_equals(prefix_set, initial_prefix_set)
    assert_equals(prefix, 'ITEST-')


def build_prefix_and_set_from_name_test():
    ''' Get prefix from element name '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
    assert_equals(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
    assert_equals(prefix_set, initial_prefix_set)
    assert_equals(prefix, 'UTEST_MY_LIB-')


def build_prefix_and_set_from_arg_test():
    ''' Get prefix from input argument `--prefix` and trim suffix of prefix '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
    assert_equals(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, 'TEST_MY_LIB_-', True, None)
    assert_equals(prefix_set, initial_prefix_set)
    assert_equals(prefix, 'TEST_MY_LIB-')


def build_prefix_and_set_from_arg_swap_set_test():
    '''
    Get prefix from input argument `--prefix` and base prefix_set on its first letter.
    Don't trim suffix of prefix.
    '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
    assert_equals(initial_prefix_set, ITEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, 'UTEST_MY_LIB_-', False, None)
    assert_not_equals(prefix_set, initial_prefix_set)
    assert_equals(prefix_set, UTEST)
    assert_equals(prefix, 'UTEST_MY_LIB_-')


def build_prefix_and_set_priority_test():
    ''' Argument unit_or_integration must have the highest priority for determining the correct prefix_set. '''
    test_suites, initial_prefix_set = parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
    assert_equals(initial_prefix_set, UTEST)

    prefix_set, prefix = build_prefix_and_set(test_suites, initial_prefix_set, 'UTEST_HOWDY-', False, 'i')
    assert_not_equals(prefix_set, initial_prefix_set)
    assert_equals(prefix_set, ITEST)
    assert_equals(prefix, 'UTEST_HOWDY-')


def verify_prefix_set_u_or_i_test():
    '''
    Tests verify_prefix_set function. The unit_or_integration argument should have the highest priority and must
    start with u or i (case-insensitive). The prefix argument has the second highest priority. A last resort is to
    keep the input prefix_set.
    '''
    assert_equals(verify_prefix_set(UTEST, 'UTEST-', 'Itest'), ITEST)
    assert_equals(verify_prefix_set(UTEST, 'UTEST-', 'i'), ITEST)
    assert_equals(verify_prefix_set(UTEST, '', 'i'), ITEST)
    assert_equals(verify_prefix_set(ITEST, 'ITEST-', 'Utest'), UTEST)
    assert_equals(verify_prefix_set(UTEST, 'ITEST-', 'u'), UTEST)
    assert_equals(verify_prefix_set(UTEST, 'UTEST-', 'u'), UTEST)
    assert_equals(verify_prefix_set(UTEST, 'BLAH-', None), UTEST)
    assert_equals(verify_prefix_set(ITEST, 'BLAH-', None), ITEST)
    assert_equals(verify_prefix_set(UTEST, 'ITEST-', None), ITEST)
    assert_equals(verify_prefix_set(ITEST, 'UTEST-', None), UTEST)
    with assert_raises(ValueError):
        verify_prefix_set(UTEST, 'UTEST-', 't')
    with assert_raises(ValueError):
        verify_prefix_set(ITEST, 'ITEST', 't')
    with assert_raises(ValueError):
        verify_prefix_set(ITEST, '', 't')


if __name__ == '__main__':
    nose.main()
