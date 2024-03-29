.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _qualification_test_report_qtest_my_lib:

==========================================
Qualification Test Report for qtest_my_lib
==========================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_QTEST_MY_LIB-MY_FUNCTION_SUCCESS Test report for QTEST_MY_LIB-MY_FUNCTION_SUCCESS
    :passes: QTEST_MY_LIB-MY_FUNCTION_SUCCESS

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_QTEST_MY_LIB-TEST_MY_FUNCTION_NOT_ERASED Test report for QTEST_MY_LIB-TEST_MY_FUNCTION_NOT_ERASED
    :fails: QTEST_MY_LIB-TEST_MY_FUNCTION_NOT_ERASED

    Test result: :xunit2rst-fail:`Fail`


.. item:: REPORT_QTEST_MY_LIB-TEST_MY_FUNCTION_NOT_UNLOCKED Test report for QTEST_MY_LIB-TEST_MY_FUNCTION_NOT_UNLOCKED
    :passes: QTEST_MY_LIB-TEST_MY_FUNCTION_NOT_UNLOCKED

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_QTEST_MY_LIB-SOME_FUNCTION Test report for QTEST_MY_LIB-SOME_FUNCTION
    :fails: QTEST_MY_LIB-SOME_FUNCTION

    Test result: :xunit2rst-fail:`Fail`


Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these qualification test reports to qualification test cases
    :source: REPORT_QTEST_MY_LIB-
    :target: QTEST_MY_LIB-
    :sourcetitle: Qualification test report
    :targettitle: Qualification test specification
    :type: fails passes skipped
    :stats:
    :group: top
    :nocaptions:
