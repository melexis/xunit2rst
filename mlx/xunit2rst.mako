<%
import textwrap
import xml.etree.ElementTree as ET

title = "{} Test Report for {}".format(info.unit_or_integration.capitalize(), report_name)

def _convert_name(name):
    """ Itemize given name and prepend prefix if needed """
    name_without_suite = name.split('.')[-1]  # cut off suite name if prepended by a dot
    converted_name = name_without_suite.upper().replace(' ', '_').replace('&', 'AND')
    if not converted_name.startswith(prefix):
        converted_name = prefix + converted_name
    return converted_name


def generate_body(input_string, error_type=None):
    ''' Transforms the input string to be part of an item's indented body with word wrapping.

    Args:
        input_string (str): Raw error message.
        error_type (str/None): The name of the error class, to be prepended to the error message if not None.

    Returns:
        str: Indented body, which has been word wrapped to not exceed 120 characters
    '''
    indent = ' ' * 4
    complete_string = "{}: {}".format(error_type, input_string) if error_type else input_string
    return indent + textwrap.fill(complete_string, 115).replace('\n', '\n' + indent).strip()
%>\
.. ${info.header_prefix}${report_name}:

${"=" * len(title)}
${title}
${"=" * len(title)}

% if log_file:
The log file that contains details about the executed test cases can be found `here <${log_file}>`_.
% endif

.. contents:: `Contents`
    :depth: 2
    :local:


Test Cases
==========

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
${generate_item(test_name, relationship, failure_message, [test])}\
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
${generate_item(test_name, relationship, failure_message, suite)}\
    % endif
% endfor
Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these ${info.unit_or_integration} test reports to ${info.unit_or_integration} test cases
    :source: REPORT_${prefix}
    :target: ${prefix}
    :sourcetitle: ${info.unit_or_integration.capitalize()} test report
    :targettitle: ${info.unit_or_integration.capitalize()} test specification
    :type: fails passes
    :stats:
    :group: top
    :nocaptions:
\
<%def name="generate_item(test_name, relationship, failure_msg, tests)">\
.. item:: REPORT_${test_name} Test report for ${test_name}
    :${relationship}: ${test_name}

    Test result: ${test_result}

        % if failure_msg:
            % for test in tests:
                % for failure in test.iterfind('failure'):
${generate_body(failure.get('message'), failure.get('type'))}

                % endfor
            %endfor
        % endif
</%def>\
