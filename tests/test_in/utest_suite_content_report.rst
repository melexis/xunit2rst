.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _unit_test_report_utest_suite_content:

========================================
Unit Test Report for utest_suite_content
========================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_UTEST_MY_LIB-SUITE_WITH_CONTENT Test report for UTEST_MY_LIB-SUITE_WITH_CONTENT
    :passes: UTEST_MY_LIB-SUITE_WITH_CONTENT

    Test result: :xunit2rst-pass:`Pass`


    .. note::
        This is extra content for the entire test suite named "SUITE_WITH_CONTENT".

        This content is defined in a .yml.mako template and demonstrates the ability
        to add RST content to test suites when using the --itemize-suites option.

        The suite contains multiple test cases but this content applies to the whole suite.

    .. code-block:: python

        # Example code that might be tested in this suite
        def example_function():
            return "Hello, World!"


.. item:: REPORT_UTEST_MY_LIB-SUITE_WITHOUT_CONTENT Test report for UTEST_MY_LIB-SUITE_WITHOUT_CONTENT
    :fails: UTEST_MY_LIB-SUITE_WITHOUT_CONTENT

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
