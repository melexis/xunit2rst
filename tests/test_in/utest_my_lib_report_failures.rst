.. _unit_test_report_utest_my_lib_report_failures:

=================================================
Unit test report for utest_my_lib_report_failures
=================================================

.. contents:: `Contents`
    :depth: 2
    :local:


.. item:: REPORT_UTEST-MY_FUNCTION_SUCCESS Test report for UTEST-MY_FUNCTION_SUCCESS
    :passes: UTEST-MY_FUNCTION_SUCCESS

    Test result: Pass

.. item:: REPORT_UTEST-MY_FUNCTION_LOCKED Test report for UTEST-MY_FUNCTION_LOCKED
    :fails: UTEST-MY_FUNCTION_LOCKED

    Test result: Fail

    File: ./unit_test/my_functions.c Line: 49 Message: exp "12 34 56 " was "12 34 99 "  and some more text to test word
    wrapping at 120 characters.

    Another failure message.

.. item:: REPORT_UTEST-SOME_FUNCTION Test report for UTEST-SOME_FUNCTION
    :fails: UTEST-SOME_FUNCTION

    Test result: Fail

    File: ./unit_test/my_functions.c Line: 49 Message: exp "12 34 56 " was "12 34 99 "

Traceability matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these unit test reports to unit test cases
    :source: REPORT_UTEST-
    :target: UTEST-
    :sourcetitle: Unit test report
    :targettitle: Unit test specification
    :type: fails passes
    :stats:
    :group:
    :nocaptions:
