.. _integration_test_report_itest_report_extra_content:

======================================================
Integration Test Report for itest_report_extra_content
======================================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_ITEST-FIRST_TEST Test report for ITEST-FIRST_TEST
    :fails: ITEST-FIRST_TEST

    Test result: Fail

    .. note::
        This note is defined in ``doc/source/extra_content.yml`` and linked to ``doc/source/robot/example.robot`` in the ``Metadata`` section as shown in the snippet below:

        .. code-block::

           Metadata         Report Info File    ../extra_content.yml


.. item:: REPORT_ITEST-AN_UNLINKED_TEST Test report for ITEST-AN_UNLINKED_TEST
    :passes: ITEST-AN_UNLINKED_TEST

    Test result: Pass

.. item:: REPORT_ITEST-ANOTHER_TEST Test report for ITEST-ANOTHER_TEST
    :passes: ITEST-ANOTHER_TEST

    Test result: Pass

    Extra content defined in `this YAML file`_, thanks to the feature :ref:`content`.

    .. _this YAML file: https://github.com/melexis/xunit2rst/blob/master/doc/source/extra_content.yml


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
