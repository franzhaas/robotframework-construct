*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using bson as an example. 
...                To run it use.:
...                uv run robot -P examples/bson/ examples/bson/simple_bson.robot
Library           bson            
Library           robotframework_construct
*** Variables ***
${bson_construct}    document
*** Test Cases ***
Example Test Case
    [Documentation]    This is an example test case.
    Register construct `${bson_construct}´ from `bson_construct´ as `bson_document´
    ${my_dict}=    Create Dictionary    hey=you
    ${blob}=    bson.encode       ${my_dict}
    ${returnedDict}=    Parse ${blob} using construct `bson_document´
    Elemement `elements.0.value´ in `${returnedDict}´ should be equal to `you´
    Run Keyword And Expect Error    *    Elemement `elements.0.value´ in `${returnedDict}´ should be equal to `me´
