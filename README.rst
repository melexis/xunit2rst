.. image:: https://travis-ci.com/melexis/xunit2rst.png?branch=master
    :target: https://travis-ci.com/melexis/xunit2rst
    :alt: Build status

.. image:: https://img.shields.io/badge/Documentation-published-brightgreen.png
    :target: https://melexis.github.io/xunit2rst/
    :alt: Documentation

.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.png
    :target: https://github.com/melexis/xunit2rst/issues
    :alt: Contributions welcome

=======================
Documentation xunit2rst
=======================

This script can convert a JUnit/xUnit (.xml) file to a reStructuredText (.rst) file with traceable items.

.. contents:: `Contents`
    :depth: 2
    :local:

----
Goal
----

This script allows you to connect your test reports to your test cases via the `mlx.traceability`_ Sphinx extension.

------------
Installation
------------

.. code-block:: console

    python3 -m pip install mlx.xunit2rst

-----
Usage
-----

Unit test report
================

.. code-block:: console

    python3 -m mlx.xunit2rst -i utest_report.xml -o utest_report.rst

Integration test report
=======================

.. code-block:: console

    python3 -m mlx.xunit2rst -i itest_report.xml -o lib_lin_itest_report.rst --prefix ITEST_LIB_LIN-

.. _`mlx.traceability`: https://pypi.org/project/mlx.traceability/
