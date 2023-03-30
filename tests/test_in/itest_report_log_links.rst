.. _integration_test_report_itest_report_log_links:

==================================================
Integration Test Report for itest_report_log_links
==================================================

The log file that contains details about the executed test cases can be found `here <itest_log.html>`_.

.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_ITEST-FIRST_TEST Test report for ITEST-FIRST_TEST
    :fails: ITEST-FIRST_TEST
    :ext_robotframeworklog: itest_log.html:s1-t1

    Test result: Fail

.. item:: REPORT_ITEST-AN_UNLINKED_TEST Test report for ITEST-AN_UNLINKED_TEST
    :passes: ITEST-AN_UNLINKED_TEST
    :ext_robotframeworklog: itest_log.html:s1-t2

    Test result: Pass

.. item:: REPORT_ITEST-ANOTHER_TEST Test report for ITEST-ANOTHER_TEST
    :passes: ITEST-ANOTHER_TEST
    :ext_robotframeworklog: itest_log.html:s1-t3

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
