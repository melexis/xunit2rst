<%
import json
from os import environ
from pathlib import Path

with open(Path(environ['TEST_IN_DIR']) / 'test_parameters.json', 'r', encoding='utf-8') as fp:
  config = json.load(fp)
%>\
Another_test: |
  Extra content defined in `this YAML file`_, thanks to the feature :ref:`content`.

  .. _this YAML file: https://github.com/melexis/xunit2rst/blob/master/doc/source/extra_content.yml
first test: |
  .. note::
      This note is defined in ``doc/source/extra_content.yml`` and linked to ``doc/source/robot/example.robot`` in the ``Metadata`` section as shown in the snippet below:

      .. code-block::

         Metadata  xunit2rst content file  ../extra_content.yml
Test voltage stepping:
<% params = config['Test voltage stepping'] %>
% for voltage in range(params['START_VOLTAGE_V'], params['STOP_VOLTAGE_V'] + 1, params['VOLTAGE_STEP_V']):
  - Successfully ran the motor ${params['ITERATIONS']} times at ${voltage} V
% endfor
COMP1-TESTING_SPECIAL_CHARACTERS_AND_PREFIX: A oneliner as extra content.
nonexistent test: This extra content shall not be used as there is no test with this name.
