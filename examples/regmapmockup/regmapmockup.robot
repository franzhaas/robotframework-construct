*** Settings ***
Documentation      This is a simple example for a robot file using constructRF demonstrating the regmap feature

Library           robotframework_construct.regmap

*** Test Cases ***
Example Test Case
    [Documentation]    This is an example test case.
    Register regmap `math_coprocessor_map´ from `math_coprocessor_regmap´ for `dsp´
    Register read register access function `read_register´ from `math_coprocessor_model´ for `dsp´
    Register write register access function `write_register´ from `math_coprocessor_model´ for `dsp´
    Read register `0` from `dsp´
    Read register `opcode` from `dsp´
    Write register `operand1` in `dsp´ with `${123}´
    Write register `operand2` in `dsp´ with `${123}´
    Write register `0` in `dsp´ with `${{ {"add": 1, "sub": 0, "mul": 0, "div": 0} }}´
    Read register `3` from `dsp´
    Write register `0` in `dsp´ with `${{ {"add": 0, "sub": 1, "mul": 0, "div": 0} }}´
    Read register `3` from `dsp´
    Write register `0` in `dsp´ with `${{ {"add": 0, "sub": 0, "mul": 1, "div": 0} }}´
    Read register `3` from `dsp´
    Write register `0` in `dsp´ with `${{ {"add": 0, "sub": 0, "mul": 0, "div": 1} }}´
    Read register `3` from `dsp´
    ${rval}=      Read register `0` from `dsp´
    Log           ${rval}
