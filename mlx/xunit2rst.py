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

TraceableInfo = namedtuple("TraceableInfo", ['matrix_prefix', 'unit_or_integration', 'header_prefix'])
UTEST = TraceableInfo('UTEST_', 'unit', '_unit_test_report_')
ITEST = TraceableInfo('ITEST_', 'integration', '_integration_test_report_')
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
    with open(str(destination), 'w', newline='\n') as rst_file:
        template = Template(filename=str(TEMPLATE_FILE), output_encoding='utf-8', input_encoding='utf-8')
        try:
            template.render_context(Context(rst_file, **kwargs))
        except Exception as exc:
            traceback = RichTraceback()
            logging.error("Exception raised in Mako template, which will be re-raised after logging line info:")
            logging.error("File %s, line %s, in %s: %r", *traceback.traceback[-1])
            raise exc


def generate_xunit_to_rst(input_file, rst_file, prefix, trim_suffix, itemize_suites, unit_or_integration):
    """ Processes input arguments, calls mako template function while passing all needed parameters.

    Args:
        input_file (Path): Path to the input file (.xml).
        rst_file (Path): Path to the output file (.rst).
        prefix (str): Prefix to add to item IDs.
        trim_suffix (bool): Whether to trim the suffix of the prefix or not.
        itemize_suites (bool): True for itemization of testsuite elements, False for testcase elements.
        unit_or_integration (None/str): None if the script's discernment shall be used, otherwise a string starting
            with 'u' or 'i', indicating unit test report or integration test report respectively as input.
    """
    test_suites, prefix_set = parse_xunit_root(input_file)

    if prefix.endswith('_-') and trim_suffix:
        prefix = prefix.rstrip('_-') + '-'

    base_prefix_on_set = False
    if not prefix:
        item_name_halves = list(test_suites)[-1].attrib['name'].split('.')[-1].split('-')
        if len(item_name_halves) > 1:
            prefix = item_name_halves[0] + '-'
        else:  # no prefix in name
            prefix = prefix_set.matrix_prefix.replace('_', '-')
            base_prefix_on_set = True

    prefix_set = _verify_prefix_set(prefix_set, unit_or_integration, prefix)
    if base_prefix_on_set:
        prefix = prefix_set.matrix_prefix.replace('_', '-')

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
    )


def parse_xunit_root(input_file):
    """
    This function parses the root element of the XML file and returns a testsuites root element and the set of prefixes
    to use.

    Args:
        input_file (Path): Path to the input file (.xml).

    Returns:
        xml.etree.ElementTree.Element: root element with testsuites as tag
        namedtuple: Set of prefixes to use for building traceability output
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

    return test_suites, prefix_set


def _verify_prefix_set(prefix_set, unit_or_integration, prefix):
    """
    The unit-or-integration test input argument has the highest priority, followed by the first letter in the prefix,
    and lastly the script will interpret a test report as a unit test report if it contains a 'testsuites' element,
    integration test report otherwise.

    Args:
        prefix_set (TraceableInfo): TraceableInfo namedtuple decided by the presence or lack of a 'testsuites' element.
        unit_or_integration (None/str): None if the script's discernment shall be used, otherwise a string starting
            with 'u' or 'i', indicating unit test report or integration test report respectively as input.
        prefix (str): Prefix that will be used in the Mako template.

    Raises:
        ValueError: The unit-or-integration argument is used, but is invalid.
    """
    if isinstance(unit_or_integration, str):
        discerning_letter = '' if not unit_or_integration else unit_or_integration.lower()[0]
    else:
        discerning_letter = prefix.lower()[0]
    if discerning_letter in 'iu':
        prefix_set = ITEST if discerning_letter == 'i' else UTEST
    elif unit_or_integration is not None:
        raise ValueError("Value for --unit-or-integration input argument is invalid: expected 'u' or 'i'; got {!r}."
                         .format(unit_or_integration))
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
                            help='The input XML file',)
    arg_parser.add_argument('-o', '--output',
                            action='store',
                            required=True,
                            dest='rst_output_file',
                            type=Path,
                            help='The output RST file',)
    arg_parser.add_argument('-s', '--itemize-suites',
                            action='store_true',
                            help="Flag to itemize testsuite elements instead of testcase elements.")
    arg_parser.add_argument('-p', '--prefix',
                            action='store',
                            default="",
                            help='Optional prefix to add to item IDs',)
    arg_parser.add_argument("--trim-suffix", action='store_true',
                            help="If the suffix of the --prefix argument ends with '_-' it gets trimmed to '-'")
    arg_parser.add_argument("--unit-or-integration", action='store',
                            help="Optional: give value starting with 'u' or 'i' if the the script's discernment is "
                                 "wrong.")
    arg_parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(version),)
    return arg_parser


def main():
    """Main function"""
    arg_parser = create_parser()
    args = arg_parser.parse_args()

    generate_xunit_to_rst(
        args.input_file,
        args.rst_output_file,
        args.prefix,
        args.trim_suffix,
        args.itemize_suites,
        args.unit_or_integration,
    )


if __name__ == "__main__":
    main()
