<%
import textwrap
import xml.etree.ElementTree as ET

title = "{} Test Report for {}".format(info.type.capitalize(), report_name)


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
    indent = ' ' * 6
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
<%
suite_names = set()
test_idx = 0
%>
% for suite_idx, suite in enumerate(test_suites, start=1):
    % if not itemize_suites:  # create traceable item per testcase element
        % for test in suite:
<%
test_name = _convert_name(test.attrib['name'])
if len(test):
    if test.findall('skipped'):
        test_result = 'Skipped'
        relationship = 'skipped'
    else:
        test_result = 'Fail'
        relationship = 'fails'
else:
    test_result = 'Pass'
    relationship = 'passes'
if add_links:
    class_name = test.attrib.get('classname', '')
    if class_name.startswith(f"{suite.attrib.get('name')}."):
        suite_name = class_name.split('.')[-1]
        if suite_name not in suite_names:
            test_idx = 0
        suite_names.add(suite_name)
test_idx += 1
%>\
${generate_item(test_name, relationship, failure_message, [test], (len(suite_names), test_idx))}\
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
    if test.findall('failure'):
        test_result = 'Fail'
        relationship = 'fails'
        break
    if test.findall('skipped'):
        test_result = 'Skipped'
        relationship = 'skipped'
%>\
${generate_item(test_name, relationship, failure_message, suite, (0, suite_idx))}\
    % endif
% endfor
Traceability Matrix
===================

The below table traces the test report to test cases.

.. item-matrix:: Linking these ${info.type} test reports to ${info.type} test cases
    :source: REPORT_${prefix}
    :target: ${prefix}
    :sourcetitle: ${info.type.capitalize()} test report
    :targettitle: ${info.type.capitalize()} test specification
    :type: fails passes
    :stats:
    :group: top
    :nocaptions:
\
<%def name="generate_item(test_name, relationship, failure_msg, tests, indexes)">\
.. item:: REPORT_${test_name} Test report for ${test_name}
    :${relationship}: ${test_name}
% if add_links:
    :ext_robotframeworklog: ${log_file}:${"s1-" if indexes[0] else ""}s${indexes[0] if indexes[0] else 1}-t${indexes[1]}
% endif

    Test result: ${test_result}
<% prepend_literal_block = True %>
% if failure_msg:
    % for test in tests:
        % for failure in test.findall('failure') + test.findall('skipped'):
            % if prepend_literal_block:
    ::
<% prepend_literal_block = False %>
            % endif
${generate_body(failure.get('message'), failure.get('type'))}

        % endfor
    %endfor
% endif
</%def>\
