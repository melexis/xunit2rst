#!/usr/bin/env python3
''' Acceptance test suite for mlx.xunit2rst

The tests in this file are pure black box tests. They just check whether the
outputs of the tool match the reference output files exactly.
'''
import filecmp
from pathlib import Path

import nose
from nose.tools import with_setup

from mlx.xunit2rst import create_parser, generate_xunit_to_rst

TOP_DIR = Path(__file__).parents[1]
TEST_OUT_DIR = Path(__file__).parent / 'test_out'
TEST_IN_DIR = Path(__file__).parent / 'test_in'


def setup():
    ''' Setup function

    This function creates the output directory for mlx.xunit2rst to put the
    output files
    '''
    TEST_OUT_DIR.mkdir(exist_ok=True)


def xunit2rst_check(input_xml, output_rst, itemize_suites=False, prefix='', trim=False, u_or_i=None, failures=False,
                    log_file=''):
    ''' Helper function for testing whether mlx.xunit2rst produces the expected output '''
    arg_parser = create_parser()
    command = ['-i', input_xml, '-o', output_rst]
    if itemize_suites:
        command.append('--itemize-suites')
    if prefix:
        command.extend(['-p', prefix])
    if trim:
        command.append('--trim-suffix')
    if u_or_i is not None:
        command.extend(['--unit-or-integration', u_or_i])
    if failures:
        command.extend(['-f'])
    if log_file:
        command.extend(['-l', log_file])
    print(command)
    args = arg_parser.parse_args(command)

    generate_xunit_to_rst(
        args.input_file,
        args.rst_output_file,
        args.itemize_suites,
        args.failure_message,
        args.log,
        args.prefix,
        args.trim_suffix,
        args.unit_or_integration,
    )


@with_setup(setup)
def test_xunit_default():
    '''Tests based on reports generated by `robot --xunit` '''
    file_name = 'itest_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='ITEST-')

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_xunit_custom_prefix():
    '''Tests based on reports generated by `robot --xunit` '''
    file_name = 'itest_lin_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='ITEST_LIN-')

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_xunit_no_prefix():
    '''Tests based on reports generated by `robot --xunit` '''
    file_name = 'itest_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_xunit_trim_suffix():
    '''Tests based on reports generated by `robot --xunit` '''
    file_name = 'itest_lin_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='ITEST_LIN_-', trim=True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_xunit_trim_suffix_not_needed():
    '''Tests based on reports generated by `robot --xunit` '''
    file_name = 'itest_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='ITEST-', trim=True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_xunit_overwrite_discernment():
    '''Tests based on reports generated by `robot --xunit` - forcing script to treat input as unit test report '''
    rst_file_name = '{}.rst'.format('itest_as_utest_report')
    xml_file_name = '{}.xml'.format('itest_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='ITEST-', u_or_i='u')

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_junit_default():
    '''Tests based on utest reports in JUnit format - itemizing testcase elements '''
    file_name = 'utest_my_lib_report'
    rst_file_name = '{}.rst'.format(file_name)
    xml_file_name = '{}.xml'.format(file_name)
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, itemize_suites=False, prefix='')

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_junit_itemize_testsuites():
    '''Tests based on utest reports in JUnit format - itemizing testsuite elements'''
    rst_file_name = '{}.rst'.format('utest_my_lib_suites_report')
    xml_file_name = '{}.xml'.format('utest_my_lib_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, itemize_suites=True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_junit_prefix():
    '''Tests based on utest reports in JUnit format - adding prefix via input arg'''
    rst_file_name = '{}.rst'.format('utest_my_lib_suites_report')
    xml_file_name = '{}.xml'.format('utest_my_lib_no_prefix_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='UTEST_MY_LIB-', itemize_suites=True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_junit_override_xml_prefix():
    '''Tests based on utest reports in JUnit format - adding prefix via input arg'''
    rst_file_name = '{}.rst'.format('utest_override_prefix_report')
    xml_file_name = '{}.xml'.format('utest_my_lib_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, prefix='OVERRIDING-')

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_xunit_failure_messages():
    '''Tests based on itest reports in xUnit format - including failure messages'''
    rst_file_name = '{}.rst'.format('itest_lin_report_failures')
    xml_file_name = '{}.xml'.format('itest_lin_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, failures=True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_junit_failure_messages():
    '''Tests based on utest reports in JUnit format - including failure messages'''
    rst_file_name = '{}.rst'.format('utest_my_lib_report_failures')
    xml_file_name = '{}.xml'.format('utest_my_lib_no_prefix_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, failures=True, itemize_suites=True)

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


@with_setup(setup)
def test_log_file():
    '''Test linking to log file'''
    rst_file_name = '{}.rst'.format('itest_report_log')
    xml_file_name = '{}.xml'.format('itest_report')
    input_xml = str(TEST_IN_DIR / xml_file_name)
    output_rst = str(TEST_OUT_DIR / rst_file_name)
    xunit2rst_check(input_xml, output_rst, log_file='itest_log.html')

    reference_rst = str(TEST_IN_DIR / rst_file_name)
    assert filecmp.cmp(output_rst, reference_rst)


if __name__ == '__main__':
    nose.main()
