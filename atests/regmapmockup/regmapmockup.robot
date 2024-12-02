*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct demonstrating the regmap feature
Library            robotframework_construct
Test Setup         prepare regmaps
Test Tags          mutation_regmap
*** Test Cases ***
Example with a simulated math coprocessor
    Write register 'operand1' in 'dsp' with '${42}'
    Write register 'operand2' in 'dsp' with '${21}'
    Write register '0' in 'dsp' with '${{ {"add": 1, "sub": 0, "mul": 0, "div": 0} }}'
    ${RESULT}=     Read register '3' from 'dsp'
    Should Be Equal As Integers    ${RESULT}    63
    Write register '0' in 'dsp' with '${{ {"add": 0, "sub": 1, "mul": 0, "div": 0} }}'
    ${RESULT}=     Read register '3' from 'dsp'
    Should Be Equal As Integers    ${RESULT}    21
    Write register '0' in 'dsp' with '${{ {"add": 0, "sub": 0, "mul": 1, "div": 0} }}'
    ${RESULT}=     Read register '3' from 'dsp'
    Should Be Equal As Integers    ${RESULT}    882
    Write register '0' in 'dsp' with '${{ {"add": 0, "sub": 0, "mul": 0, "div": 1} }}'
    ${RESULT}=     Read register '3' from 'dsp'
    Should Be Equal As Integers    ${RESULT}    2
    ${reg0}=      Read register '0' from 'dsp'
    Get element 'div' from '${reg0}'
    ${reg0}=      Modify the element located at 'div' of '${reg0}' to '${0}'
    ${reg0}=      Modify the element located at 'add' of '${reg0}' to '1'
    Write register '0' in 'dsp' with '${reg0}'
    ${RESULT}=     Read register '3' from 'dsp'
    Should Be Equal As Integers    ${RESULT}    63

remove and reload check
    Remove register map 'dsp'
    Register regmap 'math_coprocessor_map' from 'math_coprocessor_regmap' for 'dsp'

*** Keywords ***
prepare regmaps
    Register regmap 'math_coprocessor_map' from 'math_coprocessor_regmap' for 'dsp'
    Register read register access function 'read_register' from 'math_coprocessor_model' for 'dsp'
    Register write register access function 'write_register' from 'math_coprocessor_model' for 'dsp'
