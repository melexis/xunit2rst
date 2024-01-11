.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _integration_test_report_itest_lin:

=====================================
Integration Test Report for itest_lin
=====================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_ITEST_LIN-FIRST_TEST Test report for ITEST_LIN-FIRST_TEST
    :fails: ITEST_LIN-FIRST_TEST

    Test result: :xunit2rst-fail:`Fail`


.. item:: REPORT_ITEST_LIN-AN_UNLINKED_TEST Test report for ITEST_LIN-AN_UNLINKED_TEST
    :passes: ITEST_LIN-AN_UNLINKED_TEST

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_ITEST_LIN-ANOTHER_TEST Test report for ITEST_LIN-ANOTHER_TEST
    :passes: ITEST_LIN-ANOTHER_TEST

    Test result: :xunit2rst-pass:`Pass`


Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these integration test reports to integration test cases
    :source: REPORT_ITEST_LIN-
    :target: ITEST_LIN-
    :sourcetitle: Integration test report
    :targettitle: Integration test specification
    :type: fails passes skipped
    :stats:
    :group: top
    :nocaptions:
