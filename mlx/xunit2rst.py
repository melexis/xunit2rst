'''Python script that produces reStructuredText out of JUnit/xUnit output (XML)'''
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
        ERROR: Error is raised by Mako template.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(str(destination), 'w', newline='\n') as rst_file:
        template = Template(filename=str(TEMPLATE_FILE), output_encoding='utf-8', input_encoding='utf-8')
        try:
            template.render_context(Context(rst_file, **kwargs))
        except OSError:
            traceback = RichTraceback()
            for (filename, lineno, function, line) in traceback.traceback:
                logging.error("File %s, line %s, in %s", filename, lineno, function)
                logging.error(line, "\n")
            logging.error("%s: %s", str(traceback.error.__class__.__name__), traceback.error)


def generate_xunit_to_rst(input_file, rst_file, prefix, itemize_suites):
    """ Calls mako template function and passes all needed parameters.

    Args:
        input_file (Path): Path to the input file (.xml).
        rst_file (Path): Path to the output file (.rst).
        prefix (str): Prefix to add to item IDs.
        itemize_suites (bool): True for itemization of testsuite elements, False for testcase elements.
    """
    test_suites, prefix_set = parse_xunit_root(input_file)
    if not prefix and prefix_set is ITEST:
        prefix = ITEST.matrix_prefix.replace('_', '-')

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
    '''
    This function parses the root element of the XML file and returns a testsuites root element and the set of prefixes
    to use.

    Args:
        input_file (Path): Path to the input file (.xml).

    Returns:
        xml.etree.ElementTree.Element: root element with testsuites as tag
        namedtuple: Set of prefixes to use for building traceability output
    '''
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


def main():
    '''Main function'''
    try:
        version = require('mlx.xunit2rst')[0].version
    except DistributionNotFound:
        from .__xunit2rst_version__ import version
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
    arg_parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(version),)
    args = arg_parser.parse_args()

    prefix = args.prefix
    if prefix.endswith('_-') and args.trim_suffix:
        prefix = prefix.rstrip('_-') + '-'

    generate_xunit_to_rst(args.input_file, args.rst_output_file, prefix, args.itemize_suites)


if __name__ == "__main__":
    main()
