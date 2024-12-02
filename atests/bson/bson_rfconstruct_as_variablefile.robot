*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using bson as an example. 
...                To run it use.:
...                uv run robot -P examples/bson/ examples/bson/simple_bson.robot
Library            bson
Library            robotframework_construct                
Variables          bson_construct.py
*** Test Cases ***
Basic example of using a variable file to supply the construct
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${returnedDict}=    Parse '${blob}' using construct '${document}'
    Element 'elements.1.value' in '${returnedDict}' should be equal to '1'
    ${blob2}=           Generate binary from '${returnedDict}' using construct '${document}'
    Should Be Equal     ${blob}    ${blob2}
