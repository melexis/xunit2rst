<%
import xml.etree.ElementTree as ET

title = "{} test report for {}".format(info.unit_or_integration.capitalize(), report_name)

def _convert_name(name):
    """ Itemize given name and prepend prefix if needed """
    name_without_suite = name.split('.')[-1]  # cut off suite name if prepended by a dot
    converted_name = name_without_suite.upper().replace(' ', '_').replace('&', 'AND')
    if not converted_name.startswith(prefix):
        converted_name = prefix + converted_name
    return converted_name
%>\
.. ${info.header_prefix}${report_name}:

${"=" * len(title)}
${title}
${"=" * len(title)}

.. contents:: `Contents`
    :depth: 2
    :local:


% for suite in test_suites:
    % if not itemize_suites:  # create traceable item per testcase element
        % for test in suite:
<%
test_name = _convert_name(test.attrib['name'])
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
    % else:  # create traceable item per testsuite element
<%
test_result = 'Pass'
relationship = 'passes'
test_name = _convert_name(suite.attrib['name'])
# skip testsuite elements that have no testcase element (typically the first testsuite element only)
if not len(suite):
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
    :source: REPORT_${prefix}
    :target: ${prefix}
    :sourcetitle: ${info.unit_or_integration.capitalize()} test report
    :targettitle: ${info.unit_or_integration.capitalize()} test specification
    :type: fails passes
    :stats:
    :group:
    :nocaptions:
