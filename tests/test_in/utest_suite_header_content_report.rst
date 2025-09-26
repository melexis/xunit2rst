.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _unit_test_report_utest_suite_header_content:

===============================================
Unit Test Report for utest_suite_header_content
===============================================


.. note::
    **Test Suite Overview: Core Library Functions**

    This suite contains unit tests for the core functionality of MY_LIB.
    The tests verify basic operations and error handling.

    **Test Coverage:**

    - Function A: Basic functionality test
    - Function B: Edge case handling

.. warning::
    These tests require the MY_LIB library to be properly initialized.


.. important::
    **Additional Test Suite**

    This suite tests secondary functionality and known failure cases.


.. note::
    **Test Suite Overview: Core Library Functions**

    This suite contains unit tests for the core functionality of MY_LIB.
    The tests verify basic operations and error handling.

    **Test Coverage:**

    - Function A: Basic functionality test
    - Function B: Edge case handling

.. warning::
    These tests require the MY_LIB library to be properly initialized.


.. important::
    **Additional Test Suite**

    This suite tests secondary functionality and known failure cases.

.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_UTEST_MY_LIB-TEST_FUNCTION_A Test report for UTEST_MY_LIB-TEST_FUNCTION_A
    :passes: UTEST_MY_LIB-TEST_FUNCTION_A

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_UTEST_MY_LIB-TEST_FUNCTION_B Test report for UTEST_MY_LIB-TEST_FUNCTION_B
    :passes: UTEST_MY_LIB-TEST_FUNCTION_B

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_UTEST_MY_LIB-TEST_FUNCTION_C Test report for UTEST_MY_LIB-TEST_FUNCTION_C
    :fails: UTEST_MY_LIB-TEST_FUNCTION_C

    Test result: :xunit2rst-fail:`Fail`


Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these unit test reports to unit test cases
    :source: REPORT_UTEST_MY_LIB-
    :target: UTEST_MY_LIB-
    :sourcetitle: Unit test report
    :targettitle: Unit test specification
    :type: fails passes skipped
    :stats:
    :group: top
    :nocaptions:
