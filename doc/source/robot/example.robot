*** Settings ***
Documentation    Example using the space separated plain text format.
Library          OperatingSystem
Metadata         xunit2rst content file    ../extra_content.yml

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
First Test
    [Documentation]    Example of a failing test
    [Tags]             RQT-LOGGING  RQT-DIRECTORY
    Log    ${MESSAGE}
    My Keyword    /'nonexistent_'  # parsing this string in a failure message results in a Sphinx warning, unless it's in a literal code block

An Unlinked Test
    [Tags]             FUN
    Should Be Equal    ${MESSAGE}    Hello, world!

Another test
    [Documentation]    Example of a successful test
    [Tags]             RQT-SUMMATION
    ${sum}             Evaluate  ${128} + ${128}
    Should Be Equal    ${sum}    ${256}

A skipped test
    [Documentation]    Example of a test that is always skipped
    [Tags]             RQT-LOGGING
    Skip               This test case is always skipped.

*** Keywords ***
My Keyword
    [Arguments]    ${path}
    Directory Should Exist    ${path}
