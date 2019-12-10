.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache 2.0 License

.. image:: https://badge.fury.io/py/mlx.xunit2rst.png
    :target: https://badge.fury.io/py/mlx.xunit2rst
    :alt: PyPI packaged release

.. image:: https://travis-ci.com/melexis/xunit2rst.png?branch=master
    :target: https://travis-ci.com/melexis/xunit2rst
    :alt: Build status

.. image:: https://img.shields.io/badge/Documentation-published-brightgreen.png
    :target: https://melexis.github.io/xunit2rst/
    :alt: Documentation

.. image:: https://codecov.io/gh/melexis/xunit2rst/coverage.png
    :target: https://codecov.io/gh/melexis/xunit2rst
    :alt: Code Coverage

.. image:: https://requires.io/github/melexis/xunit2rst/requirements.png?branch=master
    :target: https://requires.io/github/melexis/xunit2rst/requirements/?branch=master
    :alt: Requirements Status

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

    pip3 install mlx.xunit2rst

-----
Usage
-----

Unit test report
================

.. code-block:: console

    mlx.xunit2rst -i utest_report.xml -o utest_report.rst

Integration test report
=======================

.. code-block:: console

    mlx.xunit2rst -i itest_report.xml -o lib_lin_itest_report.rst --prefix ITEST_LIB_LIN-

.. _`mlx.traceability`: https://pypi.org/project/mlx.traceability/
