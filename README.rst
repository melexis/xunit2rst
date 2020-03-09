.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache 2.0 License

.. image:: https://badge.fury.io/py/mlx.xunit2rst.svg
    :target: https://badge.fury.io/py/mlx.xunit2rst
    :alt: PyPI packaged release

.. image:: https://travis-ci.com/melexis/xunit2rst.svg?branch=master
    :target: https://travis-ci.com/melexis/xunit2rst
    :alt: Build status

.. image:: https://img.shields.io/badge/Documentation-published-brightgreen.svg
    :target: https://melexis.github.io/xunit2rst/
    :alt: Documentation

.. image:: https://codecov.io/gh/melexis/xunit2rst/coverage.svg
    :target: https://codecov.io/gh/melexis/xunit2rst
    :alt: Code Coverage

.. image:: https://requires.io/github/melexis/xunit2rst/requirements.svg?branch=master
    :target: https://requires.io/github/melexis/xunit2rst/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg
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

.. code-block:: console

    mlx.xunit2rst -i itest_report.xml -o my_lib_report.rst --prefix ITEST_MY_LIB-

    mlx.xunit2rst --help

    usage: xunit2rst [-h] -i INPUT_FILE -o RST_OUTPUT_FILE [-s] [-p PREFIX]
                     [--trim-suffix] [--unit-or-integration UNIT_OR_INTEGRATION]
                     [-f] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_FILE, --input INPUT_FILE
                            The input XML file
      -o RST_OUTPUT_FILE, --output RST_OUTPUT_FILE
                            The output RST file
      -s, --itemize-suites  Flag to itemize testsuite elements instead of testcase
                            elements.
      -p PREFIX, --prefix PREFIX
                            Optional prefix to add to item IDs
      --trim-suffix         If the suffix of the --prefix argument ends with '_-'
                            it gets trimmed to '-'
      --unit-or-integration UNIT_OR_INTEGRATION
                            Optional: give value starting with 'u' or 'i' if the
                            the script's discernment is wrong.
      -f, --failure-message
                            Include the error message in case of test failure in
                            the item's body.
      -v, --version         show program's version number and exit

.. _`mlx.traceability`: https://pypi.org/project/mlx.traceability/

--------
Behavior
--------

Itemization
===========

By default, all *testcase* elements from the input file are used to created treaceability items. This may not always be
desired. The ``-s, --itemize-suites`` flag lets the script itemize *testsuite* elements instead. In this case, the
*testcase* elements will still be parsed to determine whether the testsuite passed or failed.

Item IDs
========

The *name* attribute of the element to be itemized is used to build the item ID. Lower case letters get converted to
upper case, whitespaces get converted to underscores, and *&* characters get converted to *AND*. A valid prefix must
end with a hyphen to be recognized by the script. If there is an additional string prepended to this name by means of a
dot, this string won't be taken into account. Example below:

``MY_LIB.ITEST_MY_LIB-my function & keyword`` XML element name results in item ID
``ITEST_MY_LIB-MY_FUNCTION_AND_KEYWORD``

Prefix
======

Traceability item IDs have a prefix that is unique for the group they belong to, e.g. *ITEST_MY_LIB-*. The ``--prefix``
input argument lets you configure this prefix. It will be prepended to the item names found in the input file to build
the item ID. By default, the script adds *ITEST-* or *UTEST-* for integration or unit test reports, unless the prefixes
already exist in the input file.

Distinction between unit and integration test reports
=====================================================

Test reports that have a *testsuites* element as root in XML are treated as unit test reports. Otherwise the script
treats the input file as an integration test report. This discerning behavior gets overridden when prefixes are found in
the input file or the ``--prefix`` input argument is used. The script looks for a *U* or *I* as the first letter of the
prefix. Lastly, you can explicitly define the type by using the ``--unit-or-integration`` input argument.
Its value should start with *u* or *i* and gets parsed case-insensitively.

Include message of failure(s)
=============================

When the ``-f, --failure-message`` flag is set, the tool includes the messages of all failures of the item's test cases
in its body.
