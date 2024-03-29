.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _unit_test_report_itest_as_utest:

===================================
Unit Test Report for itest_as_utest
===================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_ITEST-FIRST_TEST Test report for ITEST-FIRST_TEST
    :fails: ITEST-FIRST_TEST

    Test result: :xunit2rst-fail:`Fail`


.. item:: REPORT_ITEST-AN_UNLINKED_TEST Test report for ITEST-AN_UNLINKED_TEST
    :passes: ITEST-AN_UNLINKED_TEST

    Test result: :xunit2rst-pass:`Pass`


.. item:: REPORT_ITEST-ANOTHER_TEST Test report for ITEST-ANOTHER_TEST
    :passes: ITEST-ANOTHER_TEST

    Test result: :xunit2rst-pass:`Pass`


Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these unit test reports to unit test cases
    :source: REPORT_ITEST-
    :target: ITEST-
    :sourcetitle: Unit test report
    :targettitle: Unit test specification
    :type: fails passes skipped
    :stats:
    :group: top
    :nocaptions:
