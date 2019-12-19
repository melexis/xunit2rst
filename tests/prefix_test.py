import xml.etree.ElementTree as ET

import nose
from nose.tools import assert_equals, assert_raises

from mlx.xunit2rst import build_prefix_and_set, verify_prefix_set, ITEST, UTEST


def build_prefix_and_set_test():
    pass


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
