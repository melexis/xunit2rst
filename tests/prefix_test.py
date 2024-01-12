#!/usr/bin/env python3
''' Test suite for functions that set the prefix and prefix_set variables '''
import unittest
from pathlib import Path

from mlx.xunit2rst import xunit2rst as dut

TEST_IN_DIR = Path(__file__).parent / 'test_in'


class TestPrefix(unittest.TestCase):
    def test_build_prefix_and_set_utest_default(self):
        ''' Use default prefix for unit test reports '''
        test_suites, initial_prefix_set, _ = dut.parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_no_prefix_report.xml')
        self.assertEqual(initial_prefix_set, dut.UTEST)

        prefix_set, prefix = dut.build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
        self.assertEqual(prefix_set, initial_prefix_set)
        self.assertEqual(prefix, 'UTEST-')

    def test_build_prefix_and_set_itest_default(self):
        ''' Use default prefix for integration test reports '''
        test_suites, initial_prefix_set, _ = dut.parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
        self.assertEqual(initial_prefix_set, dut.ITEST)

        prefix_set, prefix = dut.build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
        self.assertEqual(prefix_set, initial_prefix_set)
        self.assertEqual(prefix, 'ITEST-')

    def test_build_prefix_and_set_from_name(self):
        ''' Get prefix from element name '''
        test_suites, initial_prefix_set, _ = dut.parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
        self.assertEqual(initial_prefix_set, dut.UTEST)

        prefix_set, prefix = dut.build_prefix_and_set(test_suites, initial_prefix_set, '', True, None)
        self.assertEqual(prefix_set, initial_prefix_set)
        self.assertEqual(prefix, 'UTEST_MY_LIB-')

    def test_build_prefix_and_set_from_arg(self):
        ''' Get prefix from input argument `--prefix` and trim suffix of prefix '''
        test_suites, initial_prefix_set, _ = dut.parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
        self.assertEqual(initial_prefix_set, dut.UTEST)

        prefix_set, prefix = dut.build_prefix_and_set(test_suites, initial_prefix_set, 'TEST_MY_LIB_-', True, None)
        self.assertEqual(prefix_set, initial_prefix_set)
        self.assertEqual(prefix, 'TEST_MY_LIB-')

    def test_build_prefix_and_set_from_arg_swap_set(self):
        '''
        Get prefix from input argument `--prefix` and base prefix_set on its first letter.
        Don't trim suffix of prefix.
        '''
        test_suites, initial_prefix_set, _ = dut.parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
        self.assertEqual(initial_prefix_set, dut.ITEST)

        prefix_set, prefix = dut.build_prefix_and_set(test_suites, initial_prefix_set, 'UTEST_MY_LIB_-', False, None)
        self.assertNotEqual(prefix_set, initial_prefix_set)
        self.assertEqual(prefix_set, dut.UTEST)
        self.assertEqual(prefix, 'UTEST_MY_LIB_-')

    def test_build_prefix_and_set_priority(self):
        ''' Argument --type must have the highest priority for determining the correct prefix_set. '''
        test_suites, initial_prefix_set, _ = dut.parse_xunit_root(TEST_IN_DIR / 'utest_my_lib_report.xml')
        self.assertEqual(initial_prefix_set, dut.UTEST)

        prefix_set, prefix = dut.build_prefix_and_set(test_suites, initial_prefix_set, 'UTEST_HOWDY-', False, 'i')
        self.assertNotEqual(prefix_set, initial_prefix_set)
        self.assertEqual(prefix_set, dut.ITEST)
        self.assertEqual(prefix, 'UTEST_HOWDY-')

    def test_content_files(self):
        ''' Test the extraction of the content file path '''
        _, _, content_files = dut.parse_xunit_root(TEST_IN_DIR / 'qtest_my_lib_report.xml')
        self.assertEqual(content_files, {3: Path("../../doc/source/extra_content.yml")})

    def test_content_files_no_root(self):
        ''' Test the extraction of the content file path when the XML has no valid root element '''
        _, _, content_files = dut.parse_xunit_root(TEST_IN_DIR / 'itest_report.xml')
        self.assertEqual(content_files, {0: Path('./extra_content1.yml')})

    def test_verify_prefix_set(self):
        '''
        Tests verify_prefix_set function. The --type argument should have the highest priority and must
        start with u/i/q (case-insensitive). The prefix argument has the second highest priority. A last resort is to
        keep the input prefix_set.
        '''
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'UTEST-', 'Itest'), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'UTEST-', 'i'), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, '', 'i'), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.ITEST, 'ITEST-', 'Utest'), dut.UTEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'ITEST-', 'u'), dut.UTEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'UTEST-', 'u'), dut.UTEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'BLAH-', None), dut.UTEST)
        self.assertEqual(dut.verify_prefix_set(dut.ITEST, 'BLAH-', None), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'ITEST-', None), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.ITEST, 'UTEST-', None), dut.UTEST)
        self.assertEqual(dut.verify_prefix_set(dut.ITEST, 'QTEST-', None), dut.QTEST)
        self.assertEqual(dut.verify_prefix_set(dut.ITEST, 'ITEST-', 'q'), dut.QTEST)
        self.assertEqual(dut.verify_prefix_set(dut.UTEST, 'UTEST-', 'Qtest'), dut.QTEST)
        self.assertEqual(dut.verify_prefix_set(dut.QTEST, '', 'u'), dut.UTEST)
        self.assertEqual(dut.verify_prefix_set(dut.QTEST, '', 'i'), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.QTEST, 'UTEST', 'i'), dut.ITEST)
        self.assertEqual(dut.verify_prefix_set(dut.QTEST, 'FOO-', None), dut.QTEST)
        with self.assertRaises(ValueError):
            dut.verify_prefix_set(dut.UTEST, 'UTEST-', 't')
        with self.assertRaises(ValueError):
            dut.verify_prefix_set(dut.ITEST, 'ITEST', 't')
        with self.assertRaises(ValueError):
            dut.verify_prefix_set(dut.ITEST, '', '')
        with self.assertRaises(ValueError):
            dut.verify_prefix_set(dut.QTEST, '', 't')


if __name__ == '__main__':
    unittest.main()
