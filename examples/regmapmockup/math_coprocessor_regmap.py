import construct


math_coprocessor_map = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(28)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )
