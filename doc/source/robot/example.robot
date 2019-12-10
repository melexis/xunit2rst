*** Settings ***
Documentation    Example using the space separated plain text format.
Library          OperatingSystem

*** Variables ***
${MESSAGE}       Hello, world!

*** Test Cases ***
First Test
    [Documentation]    Example of a failing test
    [Tags]             RQT-LOGGING  RQT-DIRECTORY
    Log    ${MESSAGE}
    My Keyword    /nonexistent

An Unlinked Test
    [Tags]             FUN
    Should Be Equal    ${MESSAGE}    Hello, world!

Another test
    [Documentation]    Example of a successful test
    [Tags]             RQT-SUMMATION
    ${sum}             Evaluate  ${128} + ${128}
    Should Be Equal    ${sum}    ${256}

*** Keywords ***
My Keyword
    [Arguments]    ${path}
    Directory Should Exist    ${path}
