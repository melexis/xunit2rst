.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _unit_test_report_utest_my_lib_report_skipped:

================================================
Unit Test Report for utest_my_lib_report_skipped
================================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_UTEST_MY_LIB-MY_FUNCTION_SUCCESS Test report for UTEST_MY_LIB-MY_FUNCTION_SUCCESS
    :skipped: UTEST_MY_LIB-MY_FUNCTION_SUCCESS

    Test result: :xunit2rst-skip:`Skip`


.. item:: REPORT_UTEST_MY_LIB-TEST_MY_FUNCTION_NOT_ERASED Test report for UTEST_MY_LIB-TEST_MY_FUNCTION_NOT_ERASED
    :skipped: UTEST_MY_LIB-TEST_MY_FUNCTION_NOT_ERASED

    Test result: :xunit2rst-skip:`Skip`


.. item:: REPORT_UTEST_MY_LIB-TEST_MY_FUNCTION_NOT_UNLOCKED Test report for UTEST_MY_LIB-TEST_MY_FUNCTION_NOT_UNLOCKED
    :passes: UTEST_MY_LIB-TEST_MY_FUNCTION_NOT_UNLOCKED

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_UTEST_MY_LIB-SOME_FUNCTION1 Test report for UTEST_MY_LIB-SOME_FUNCTION1
    :fails: UTEST_MY_LIB-SOME_FUNCTION1

    Test result: :xunit2rst-fail:`Fail`


.. item:: REPORT_UTEST_MY_LIB-SOME_FUNCTION2 Test report for UTEST_MY_LIB-SOME_FUNCTION2
    :skipped: UTEST_MY_LIB-SOME_FUNCTION2

    Test result: :xunit2rst-skip:`Skip`


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
