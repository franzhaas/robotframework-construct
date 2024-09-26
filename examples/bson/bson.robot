*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using bson as an example. 
...                To run it use.:
...                uv run robot -P examples/bson/ examples/bson/simple_bson.robot
Library            bson            
Library            robotframework_construct
Test Setup         Prepare test case
*** Variables ***
${bson_construct}    document
*** Test Cases ***


Invalid parse input type
    [Documentation]    This is an example test case.
    Run Keyword And Expect Error    could not convert `1´ to io.BytesIO:*      Parse `${1}´ using construct `bson_document´
    
Simple positive element checks
    Elemement `elements.1.value´ in `${returnedDict}´ should be equal to `1´
    Elemement `elements.1.value´ in `${returnedDict}´ should not be equal to `0´
    Elemement `elements.1.value´ in `${returnedDict}´ should not be equal to `2´
    Elemement `elements.0.value´ in `${returnedDict}´ should be equal to `you´
    Elemement `elements.0.value´ in `${returnedDict}´ should not be equal to `me´
    
Simple negative element checks
    Run Keyword And Expect Error    could not convert*           Elemement `elements.1.value´ in `${returnedDict}´ should be equal to `one´
    Run Keyword And Expect Error    *does not match expected*    Elemement `elements.1.value´ in `${returnedDict}´ should be equal to `0´
    Run Keyword And Expect Error    *does not match expected*    Elemement `elements.1.value´ in `${returnedDict}´ should be equal to `2´
    Run Keyword And Expect Error    *is not distinct to*         Elemement `elements.0.value´ in `${returnedDict}´ should not be equal to `you´
    Run Keyword And Expect Error    *does not match expected*    Elemement `elements.0.value´ in `${returnedDict}´ should be equal to `me´

Checks involving modifications
    Modify the elemement located at `elements.0.value´ of `${returnedDict}´ to `me´
    Elemement `elements.0.value´ in `${returnedDict}´ should be equal to `me´
    
    Run Keyword And Expect Error    could not convert*    Modify the elemement located at `elements.1.value´ of `${returnedDict}´ to `two´
    Run Keyword And Expect Error    could not find*    Modify the elemement located at `elements.2.value´ of `${returnedDict}´ to `two´

Modifying the element seperator
    Run Keyword And Expect Error    could not find*    Get elemement `elements->0->value´ from `${returnedDict}´
    Set element seperator to `->´
    Run Keyword And Expect Error    *    Modify the elemement located at `elements.0.value´ of `${returnedDict}´ to `me´
    Elemement `elements->0->value´ in `${returnedDict}´ should be equal to `you´
    Modify the elemement located at `elements->0->value´ of `${returnedDict}´ to `me´
    Elemement `elements->0->value´ in `${returnedDict}´ should be equal to `me´
    Get elemement `elements->0->value´ from `${returnedDict}´
    Run Keyword And Expect Error    *        Get elemement `elements->0->valueXX from `${returnedDict}´

Generate binary
    ${generated}=     Generate binary from `${returnedDict}´ using construct `bson_document´
    Should Be Equal   ${generated}     ${blob}


*** Keywords ***
Prepare test case
    Register construct `${bson_construct}´ from `bson_construct´ as `bson_document´
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${returnedDict}=    Parse `${blob}´ using construct `bson_document´
    Set Task Variable   ${blob}           ${blob}
    Set Task Variable   ${my_dict}        ${my_dict}
    Set Task Variable   ${returnedDict}   ${returnedDict}