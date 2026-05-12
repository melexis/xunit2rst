.. role:: xunit2rst-skip
    :class: xunit2rst skip
.. role:: xunit2rst-fail
    :class: xunit2rst fail
.. role:: xunit2rst-pass
    :class: xunit2rst pass

.. _integration_test_report_itest_report_testcase_extra_content:

===============================================================
Integration Test Report for itest_report_testcase_extra_content
===============================================================


.. contents:: `Contents`
    :depth: 2
    :local:


Test Reports
============

.. item:: REPORT_ITEST-PWM_SYNC_IN_PIN_TO_SLAVE_TIMING Test report for ITEST-PWM_SYNC_IN_PIN_TO_SLAVE_TIMING
    :passes: ITEST-PWM_SYNC_IN_PIN_TO_SLAVE_TIMING

    Test result: :xunit2rst-pass:`Pass`


    The plots below display the captured SYNC IN and slave PWM output signals for different external PWM frequencies.

    .. figure:: sync_in_signal_800.png
      :height: 300px
      :align: center
      :alt: PWM signals
      :figclass: align-center

    .. figure:: sync_in_signal_1000.png
      :height: 300px
      :align: center
      :alt: PWM signals
      :figclass: align-center

    .. figure:: sync_in_signal_1200.png
      :height: 300px
      :align: center
      :alt: PWM signals
      :figclass: align-center

    The plots below display the time difference (gap) between the rising edge of the SYNC IN signal and the falling edge of the slave PWM output signal.

    .. figure:: sync_in_timing_800.png
      :height: 300px
      :align: center
      :alt: PWM signals
      :figclass: align-center

    .. figure:: sync_in_timing_1000.png
      :height: 300px
      :align: center
      :alt: PWM signals
      :figclass: align-center

    .. figure:: sync_in_timing_1200.png
      :height: 300px
      :align: center
      :alt: PWM signals
      :figclass: align-center


.. item:: REPORT_ITEST-PWM_MASTER_TO_SYNC_PIN_TIMING Test report for ITEST-PWM_MASTER_TO_SYNC_PIN_TIMING
    :passes: ITEST-PWM_MASTER_TO_SYNC_PIN_TIMING

    Test result: :xunit2rst-pass:`Pass`


    The plot below displays the captured PWM master and PWM SYNC output signal.

    .. figure:: sync_out_signal.png
      :height: 600px
      :align: center
      :alt: PWM signals
      :figclass: align-center

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
