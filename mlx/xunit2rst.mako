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


def generate_body(input_string, indent, error_type=None):
    ''' Transforms the input string to be part of an item's indented body with word wrapping.

    Args:
        input_string (str): Raw error message.
        error_type (str/None): The name of the error class, to be prepended to the error message if not None.

    Returns:
        str: Indented body, which has been word wrapped to not exceed 120 characters
    '''
    complete_string = "{}: {}".format(error_type, input_string) if error_type else input_string
    wrapped = textwrap.fill(complete_string, width=(119 - len(indent)), break_on_hyphens=False, break_long_words=False)
    return textwrap.indent(wrapped, indent)
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


Test Reports
============
<%
suite_names = set()
test_idx = 0
%>
% for suite_idx, suite in enumerate(test_suites):
<% print(suite_idx); extra_content_map = indexed_extra_content_map.get(suite_idx, {}) %>\
    % if not itemize_suites:  # create traceable item per testcase element
        % for test in suite:
<%
if len(test):
    if test.findall('skipped'):
        test_result = 'Skip'
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
${generate_item(test.attrib['name'], relationship, failure_message, [test], (len(suite_names), test_idx), extra_content_map)}\
        % endfor
    % else:  # create traceable item per testsuite element
<%
test_result = 'Pass'
relationship = 'passes'
# skip testsuite elements that have no testcase element (typically the first testsuite element only)
if not len(suite):
    continue

skipped_counter = 0
for test in suite:
    if test.findall('failure'):
        test_result = 'Fail'
        relationship = 'fails'
        break
    if test.findall('skipped'):
        skipped_counter += 1
else:
    if skipped_counter == len(suite):
        test_result = 'Skip'
        relationship = 'skipped'
%>\
${generate_item(suite.attrib['name'], relationship, failure_message, suite, (0, suite_idx + 1), extra_content_map)}\
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
    :type: fails passes skipped
    :stats:
    :group: top
    :nocaptions:
\
<%def name="generate_item(element_name, relationship, failure_msg, tests, indexes, extra_content_map)">\
<%
test_name = _convert_name(element_name)
key_name = element_name.lower().replace(' ', '_')
extra_content = extra_content_map.get(key_name, "")
%>\
.. item:: REPORT_${test_name} Test report for ${test_name}
    :${relationship}: ${test_name}
% if add_links:
    :ext_robotframeworklog: ${log_file}:${"s1-" if indexes[0] else ""}s${indexes[0] if indexes[0] else 1}-t${indexes[1]}
% endif

    Test result: ${test_result}
<% prepend_literal_block = True %>
% if failure_msg and relationship != 'passes':
    % for test in tests:
        % for failure in test.findall('failure') + test.findall('skipped'):
            % if prepend_literal_block:
    ::
<% prepend_literal_block = False %>
            % endif
${generate_body(failure.get('message'), ' ' * 6, error_type=failure.get('type'))}

        % endfor
    % endfor
% endif
% if extra_content:
${textwrap.indent(extra_content, ' ' * 4)}

% endif
</%def>\
