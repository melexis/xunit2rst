.. _integration_test_report_itest_lin_report_failures:

=====================================================
Integration Test Report for itest_lin_report_failures
=====================================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_ITEST-FIRST_TEST Test report for ITEST-FIRST_TEST
    :fails: ITEST-FIRST_TEST

    Test result: Fail

    ::

      AssertionError: Directory 'C:\nonexistent' does not exist.

      Error: Second failure

.. item:: REPORT_ITEST-AN_UNLINKED_TEST Test report for ITEST-AN_UNLINKED_TEST
    :passes: ITEST-AN_UNLINKED_TEST

    Test result: Pass

.. item:: REPORT_ITEST-ANOTHER_TEST Test report for ITEST-ANOTHER_TEST
    :passes: ITEST-ANOTHER_TEST

    Test result: Pass

Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these integration test reports to integration test cases
    :source: REPORT_ITEST-
    :target: ITEST-
    :sourcetitle: Integration test report
    :targettitle: Integration test specification
    :type: fails passes skipped
    :stats:
    :group: top
    :nocaptions:
