.. _unit_test_report_utest_my_lib_suites_report_skipped:

=======================================================
Unit Test Report for utest_my_lib_suites_report_skipped
=======================================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_UTEST_MY_LIB-MY_FUNCTION_SUCCESS Test report for UTEST_MY_LIB-MY_FUNCTION_SUCCESS
    :skipped: UTEST_MY_LIB-MY_FUNCTION_SUCCESS

    Test result: Skip

    ::

      Skipping the sole test case in this test suite.

.. item:: REPORT_UTEST_MY_LIB-MY_FUNCTION_LOCKED Test report for UTEST_MY_LIB-MY_FUNCTION_LOCKED
    :passes: UTEST_MY_LIB-MY_FUNCTION_LOCKED

    Test result: Pass

.. item:: REPORT_UTEST_MY_LIB-SOME_FUNCTION Test report for UTEST_MY_LIB-SOME_FUNCTION
    :fails: UTEST_MY_LIB-SOME_FUNCTION

    Test result: Fail

    ::

      File: ./unit_test/my_functions.c Line: 49 Message: exp "12 34 56 " was "12 34 99 "

      Skipping this test case but the other test case in this suite should fail.

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
