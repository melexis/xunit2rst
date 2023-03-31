"""Python script that produces reStructuredText out of JUnit/xUnit output (XML)"""
import argparse
import logging
import xml.etree.ElementTree as ET
from collections import namedtuple
from pathlib import Path
from textwrap import indent

from mako.exceptions import RichTraceback
from mako.template import Template
from pkg_resources import DistributionNotFound, require
from ruamel.yaml import YAML

TraceableInfo = namedtuple("TraceableInfo", ['matrix_prefix', 'type', 'header_prefix'])
UTEST = TraceableInfo('UTEST_', 'unit', '_unit_test_report_')
ITEST = TraceableInfo('ITEST_', 'integration', '_integration_test_report_')
QTEST = TraceableInfo('QTEST_', 'qualification', '_qualification_test_report_')
TEMPLATE_FILE = Path(__file__).parent.joinpath('xunit2rst.mako')


def render_template(destination, only="", **kwargs):
    """ Renders the Mako template, and writes output file to the specified destination.

    Args:
        destination (Path): Location of the output file.
        only (str): Expression for 'only' directive, which will only be added when this string is not empty.
        **kwargs (dict): Variables to be used in the Mako template.

    Raises:
        ERROR: Error log containing information about the line where the exception occurred.
        Exception: Re-raised Exception coming from Mako template.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    template = Template(filename=str(TEMPLATE_FILE))
    try:
        rst_content = template.render(**kwargs)
    except Exception as exc:
        traceback = RichTraceback()
        logging.error("Exception raised in Mako template, which will be re-raised after logging line info:")
        logging.error("File %s, line %s, in %s: %r", *traceback.traceback[-1])
        raise exc
    if only:
        rst_content = f".. only:: {only}\n\n{indent(rst_content, ' ' * 4)}"
    with open(str(destination), 'w', encoding='utf-8', newline='\n') as rst_file:
        rst_file.write(rst_content)


def generate_xunit_to_rst(input_file, rst_file, itemize_suites, failure_message, log_file, add_links, *prefix_args,
                          **kwargs):
    """ Processes input arguments, calls mako template function while passing all needed parameters.

    Args:
        input_file (Path): Path to the input file (.xml).
        rst_file (Path): Path to the output file (.rst).
        itemize_suites (bool): True for itemization of testsuite elements, False for testcase elements.
        failure_message (bool): True if failure messages are to be included in the item's body, False otherwise.
        log_file (str): Optional path to the HTML log file, empty when not specified.
        add_links (bool): True to add links to the HTML log file for each test case
    """
    test_suites, prefix_set, report_info_files = parse_xunit_root(input_file)

    prefix_set, prefix = build_prefix_and_set(test_suites, prefix_set, *prefix_args)

    report_name = rst_file.stem
    if report_name.endswith('_report'):
        report_name = report_name[:-len('_report')]

    indexed_extra_content_map = {}
    for i, file in report_info_files.items():
        extra_content_map = {}
        yaml = YAML(typ='safe', pure=True)
        if not file.is_absolute():
            file = input_file.parent / file
        extra_content_map = {name.lower().replace(' ', '_'): content
                             for name, content in yaml.load(file).items()}
        indexed_extra_content_map[i] = extra_content_map

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
        indexed_extra_content_map=indexed_extra_content_map,
        **kwargs,
    )


def look_for_content_file(element):
    """ If the element contains metadata, it returns the path to the content file, if configured.

    Args:
        element (xml.etree.ElementTree.Element): XML element to inspect

    Returns:
        Path/None: Path to the content file, if found in the given element; None otherwise
    """
    if element.tag in ('properties', 'traits'):
        for prop in element:
            if prop.attrib['name'].lower() == 'xunit2rst content file':
                return Path(prop.attrib['value'])


def parse_xunit_root(input_file):
    """
    This function parses the root element of the XML file and returns the root element, which contains one or more
    'testsuite' elements, and the set of prefixes to use.

    Note: only the root element and elements with tag 'testsuite' and 'testcase' are included. The tag of the root
    element does not matter.

    Args:
        input_file (Path): Path to the input file (.xml).

    Returns:
        xml.etree.ElementTree.Element: Root element of the element tree, which contains 'testsuite' elements.
        TraceableInfo: Namedtuple holding the prefixes to use for building traceability output.
        dict: Mapping of testsuite index to the Path to the content files; empty when none are configured
    """
    tree = ET.parse(str(input_file))
    root_input = tree.getroot()
    if root_input.find('testsuite') is None:
        test_suites = ET.Element("root")
        test_suites.append(root_input)
        prefix_set = ITEST
    else:
        test_suites = root_input
        prefix_set = UTEST

    report_info_files = {}
    for i, suite in enumerate(test_suites):
        if suite.tag != 'testsuite':
            test_suites.remove(suite)
            continue
        for test in suite:
            if test.tag != 'testcase':
                value = look_for_content_file(test)
                if value:
                    report_info_files[i] = value
                suite.remove(test)
    return test_suites, prefix_set, report_info_files


def build_prefix_and_set(test_suites, prefix_set, prefix, trim_suffix, type_):
    """ Builds the prefix and prefix_set variables based on the input parameters.

    Args:
        test_suites (xml.etree.ElementTree.Element): Root element of the element tree, which contains one or more
            'testsuite' elements.
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
        test_suite = list(test_suites)[-1]
        test_suite_name = test_suite.attrib.get('name', '')
        name_parts = test_suite_name.split('.')[-1].split('-')
        if len(name_parts) > 1:
            prefix = name_parts[0] + '-'
        else:  # test suite has no name or does not contain a prefix
            prefix = prefix_set.matrix_prefix
            base_prefix_on_set = True

    prefix_set = verify_prefix_set(prefix_set, prefix, type_)
    if base_prefix_on_set:
        prefix = prefix_set.matrix_prefix
    prefix = prefix.rstrip('_')
    if not prefix.endswith('-'):
        prefix += '-'
    return prefix_set, prefix


def verify_prefix_set(prefix_set, prefix, type_):
    """
    The --type input argument has the highest priority, followed by the first letter in the prefix,
    and lastly the given prefix_set will be used.

    Args:
        prefix_set (TraceableInfo): TraceableInfo UTEST or ITEST decided by whether the 'testsuite' elements have a
            parent element.
        prefix (str): Prefix that will be used in the Mako template.
        type_ (None/str): None if the script's discernment shall be used, otherwise a string starting
            with 'u'/'i'/'q', indicating that the input contains unit/integration/qualification tests respectively.

    Returns:
        TraceableInfo: namedtuple that contains prefix and other info regarding the type of test

    Raises:
        ValueError: The --type argument is used, but is invalid.
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
    arg_parser.add_argument("--only", dest="expression", default="",
                            help="Expression of tags for Sphinx' `only` directive that surrounds all RST content. "
                            "By default, no `only` directive is generated.")
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
        only=args.expression,
    )


if __name__ == "__main__":
    main()
