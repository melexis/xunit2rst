<%
# This is a Mako template for testing suite content
%>\
UTEST_MY_LIB-SUITE_WITH_CONTENT: |
  .. note::
      This is extra content for the entire test suite named "SUITE_WITH_CONTENT".

      This content is defined in a .yml.mako template and demonstrates the ability
      to add RST content to test suites when using the --itemize-suites option.

      The suite contains multiple test cases but this content applies to the whole suite.

  .. code-block:: python

      # Example code that might be tested in this suite
      def example_function():
          return "Hello, World!"
