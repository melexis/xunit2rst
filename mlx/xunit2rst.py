"""Python script that produces reStructuredText out of JUnit/xUnit output (XML)"""
import argparse
import logging
import xml.etree.ElementTree as ET
from collections import namedtuple
from pathlib import Path

from mako.exceptions import RichTraceback
from mako.runtime import Context
from mako.template import Template
from pkg_resources import DistributionNotFound, require

TraceableInfo = namedtuple("TraceableInfo", ['matrix_prefix', 'type', 'header_prefix'])
UTEST = TraceableInfo('UTEST_', 'unit', '_unit_test_report_')
ITEST = TraceableInfo('ITEST_', 'integration', '_integration_test_report_')
QTEST = TraceableInfo('QTEST_', 'qualification', '_qualification_test_report_')
TEMPLATE_FILE = Path(__file__).parent.joinpath('xunit2rst.mako')


def render_template(destination, **kwargs):
    """ Renders the Mako template, and writes output file to the specified destination.

    Args:
        destination (Path): Location of the output file.
        **kwargs (dict): Variables to be used in the Mako template.

    Raises:
        ERROR: Error log containing information about the line where the exception occurred.
        Exception: Re-raised Exception coming from Mako template.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(str(destination), 'w', newline='\n', encoding='utf-8') as rst_file:
        template = Template(filename=str(TEMPLATE_FILE), output_encoding='utf-8', input_encoding='utf-8')
        try:
            template.render_context(Context(rst_file, **kwargs))
        except Exception as exc:
            traceback = RichTraceback()
            logging.error("Exception raised in Mako template, which will be re-raised after logging line info:")
            logging.error("File %s, line %s, in %s: %r", *traceback.traceback[-1])
            raise exc


def generate_xunit_to_rst(input_file, rst_file, itemize_suites, failure_message, log_file, add_links, *prefix_args):
    """ Processes input arguments, calls mako template function while passing all needed parameters.

    Args:
        input_file (Path): Path to the input file (.xml).
        rst_file (Path): Path to the output file (.rst).
        itemize_suites (bool): True for itemization of testsuite elements, False for testcase elements.
        failure_message (bool): True if failure messages are to be included in the item's body, False otherwise.
        log_file (str): Optional path to the HTML log file, empty when not specified.
        add_links (bool): True to add links to the HTML log file for each test case
    """
    test_suites, prefix_set = parse_xunit_root(input_file)

    prefix_set, prefix = build_prefix_and_set(test_suites, prefix_set, *prefix_args)

    report_name = rst_file.stem
    if report_name.endswith('_report'):
        report_name = report_name[:-len('_report')]

    render_template(
        rst_file,
        test_suites=test_suites,
        report_name=report_name,
        info=prefix_set,
        prefix=prefix,
        itemize_suites=itemize_suites,
        failure_message=failure_message,
        log_file=log_file,
        add_links=add_links,
    )


def parse_xunit_root(input_file):
    """
    This function parses the root element of the XML file and returns a testsuites root element and the set of prefixes
    to use.

    Note: only elements with tag 'testsuites', 'testsuite' and 'testcase' are included.

    Args:
        input_file (Path): Path to the input file (.xml).

    Returns:
        xml.etree.ElementTree.Element: Root element of the element tree with 'testsuites' as tag.
        TraceableInfo: Namedtuple holding the prefixes to use for building traceability output.
    """
    tree = ET.parse(str(input_file))
    root_input = tree.getroot()
    if root_input.tag != 'testsuites':
        test_suites = ET.Element("testsuites")
        test_suites.append(root_input)
        prefix_set = ITEST
    else:
        test_suites = root_input
        prefix_set = UTEST

    for suite in test_suites:
        if suite.tag != 'testsuite':
            test_suites.remove(suite)
            continue
        for test in suite:
            if test.tag != 'testcase':
                suite.remove(test)

    return test_suites, prefix_set


def build_prefix_and_set(test_suites, prefix_set, prefix, trim_suffix, type_):
    """ Builds the prefix and prefix_set variables based on the input parameters.

    Args:
        test_suites (xml.etree.ElementTree.Element): Root element of the element tree with 'testsuites' as tag.
        prefix_set (TraceableInfo): Namedtuple holding the default prefix to use for building traceability output.
        prefix (str): Prefix to add to item IDs. In case of an empty string, the prefix from the element's name will be
            used, or the default prefix otherwise.
        trim_suffix (bool): Whether to trim the suffix of the prefix or not.
        type_ (None/str): None if the script's discernment shall be used, otherwise a string starting
            with 'u'/'i'/'q', indicating that the input contains unit/integration/qualification tests respectively.

    Returns:
        prefix_set (TraceableInfo): Namedtuple holding the prefixes to use for building traceability output.
        prefix (str): Prefix to add to item IDs.
    """
    if prefix.endswith('_-') and trim_suffix:
        prefix = prefix.rstrip('_-') + '-'

    base_prefix_on_set = False
    if not prefix:
        item_name_halves = list(test_suites)[-1].attrib['name'].split('.')[-1].split('-')
        if len(item_name_halves) > 1:
            prefix = item_name_halves[0] + '-'
        else:  # no prefix in name
            prefix = prefix_set.matrix_prefix
            base_prefix_on_set = True

    prefix_set = verify_prefix_set(prefix_set, prefix, type_)
    if base_prefix_on_set:
        prefix = prefix_set.matrix_prefix
    prefix = prefix.rstrip('_')
    prefix = prefix + '-' if not prefix.endswith('-') else prefix
    return prefix_set, prefix


def verify_prefix_set(prefix_set, prefix, type_):
    """
    The --type input argument has the highest priority, followed by the first letter in the prefix,
    and lastly the script will interpret a test report as a unit test report if it contains a 'testsuites' element,
    integration test report otherwise.

    Args:
        prefix_set (TraceableInfo): TraceableInfo UTEST or ITEST decided by the presence or lack of a root element
            'testsuites'.
        prefix (str): Prefix that will be used in the Mako template.
        type_ (None/str): None if the script's discernment shall be used, otherwise a string starting
            with 'u'/'i'/'q', indicating that the input contains unit/integration/qualification tests respectively.

    Returns:
        TraceableInfo: namedtuple that contains prefix and other info regarding the type of test

    Raises:
        ValueError: The unit-or-integration argument is used, but is invalid.
    """
    type_map = {
        'u': UTEST,
        'i': ITEST,
        'q': QTEST,
    }
    if isinstance(type_, str):
        discerning_letter = '' if not type_ else type_.lower()[0]
    else:
        discerning_letter = prefix.lower()[0]
    if discerning_letter in type_map:
        return type_map[discerning_letter]
    elif type_ is not None:
        raise ValueError("Value for --type input argument is invalid: expected value in {}; got {!r}."
                         .format(list(type_map), type_))
    return prefix_set


def create_parser():
    """ Creates and returns the ArgumentParser instance to be used """
    try:
        version = require('mlx.xunit2rst')[0].version
    except DistributionNotFound:
        version = '0.0.0.dev'
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--input',
                            action='store',
                            required=True,
                            dest='input_file',
                            type=Path,
                            help='The input XML file')
    arg_parser.add_argument('-o', '--output',
                            action='store',
                            required=True,
                            dest='rst_output_file',
                            type=Path,
                            help='The output RST file')
    arg_parser.add_argument('-s', '--itemize-suites',
                            action='store_true',
                            help="Flag to itemize testsuite elements instead of testcase elements.")
    arg_parser.add_argument('-p', '--prefix',
                            action='store',
                            default="",
                            help='Optional prefix to add to item IDs')
    arg_parser.add_argument("--trim-suffix", action='store_true',
                            help="If the suffix of the --prefix argument ends with '_-' it gets trimmed to '-'")
    arg_parser.add_argument("--unit-or-integration", action='store',
                            help="Deprecated alternative to --type; to be removed in version 2.0.0.")
    arg_parser.add_argument("-t", "--type", action='store',
                            help="Optional: give value starting with 'u', 'i' or 'q' to explicitly define the type "
                            "of test: unit/integration/qualification test")
    arg_parser.add_argument("-f", "--failure-message", action="store_true",
                            help="Include the error message in case of test failure in the item's body.")
    arg_parser.add_argument("-l", "--log", action="store",
                            help="Optional: path to the HTML log file, relative to where Sphinx will put the --output, "
                                 "to create a link to.")
    arg_parser.add_argument("--links", action="store_true",
                            help="Optional: inserts a link to the RobotFramework HTML log file for each test case "
                                 "as ext_robotframeworklog link id.")
    arg_parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(version))
    return arg_parser


def main():
    """Main function"""
    arg_parser = create_parser()
    args = arg_parser.parse_args()
    if args.unit_or_integration and not args.type:
        args.type = args.unit_or_integration
        logging.warning('Deprecation warning: --unit-or-integration will be removed in version 2.0.0; use --type')
    generate_xunit_to_rst(
        args.input_file,
        args.rst_output_file,
        args.itemize_suites,
        args.failure_message,
        args.log,
        args.links,
        args.prefix,
        args.trim_suffix,
        args.type,
    )


if __name__ == "__main__":
    main()
