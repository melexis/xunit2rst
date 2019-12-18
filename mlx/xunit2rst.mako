<%
import xml.etree.ElementTree as ET

title = "{} test report for {}".format(info.unit_or_integration.capitalize(), report_name)


def _convert_name(name, prefix="", utest=False):
    if utest and '.' not in name:
        return None
    name = name.split('.')[-1]  # cut off suite name if prepended by a dot
    return prefix + name.upper().replace(' ', '_').replace('&', 'AND')
%>\
.. ${info.header_prefix}${report_name}:

${"=" * len(title)}
${title}
${"=" * len(title)}

.. contents:: `Contents`
    :depth: 2
    :local:

<%
if info.unit_or_integration == 'unit':
    target_prefix = info.matrix_prefix + list(test_suites)[0].attrib['name']
else:
    target_prefix = prefix
%>\

% for suite in test_suites:
    % if not itemize_suites:  # create traceable item per testcase element
        % for test in suite:
<%
test_name = _convert_name(test.attrib['name'], prefix=prefix)
if len(test):
    test_result = 'Fail'
    relationship = 'fails'
else:
    test_result = 'Pass'
    relationship = 'passes'
%>\
.. item:: REPORT_${test_name} Test report for ${test_name}
    :${relationship}: ${test_name}

    Test result: ${test_result}

        % endfor
    % else:  # create traceable item per testsuite tag
<%
test_result = 'Pass'
relationship = 'passes'
test_name = _convert_name(suite.attrib['name'], prefix=prefix, utest=True)
if not test_name:
    continue

for test in suite:
    if len(test):
        test_result = 'Fail'
        relationship = 'fails'
        break
%>\
.. item:: REPORT_${test_name} Test report for ${test_name}
    :${relationship}: ${test_name}

    Test result: ${test_result}

    % endif
% endfor
Traceability matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these ${info.unit_or_integration} test reports to ${info.unit_or_integration} test cases
    :source: REPORT_${target_prefix}
    :target: ${target_prefix}
    :sourcetitle: ${info.unit_or_integration.capitalize()} test report
    :targettitle: ${info.unit_or_integration.capitalize()} test specification
    :type: fails passes
    :stats:
    :group:
    :nocaptions:
