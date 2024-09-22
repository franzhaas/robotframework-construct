from construct import Struct, Int8ul, Int8sl, Int32sl, Int64sl, Int64ul, Float64l, Array, Byte, GreedyBytes, CString, Prefixed, Switch, this, LazyBound, Pass, GreedyRange, Rebuild, len_, this

# Basic Types
byte = Byte
signed_byte = Int8sl
unsigned_byte = Int8ul
int32 = Int32sl
int64 = Int64sl
uint64 = Int64ul
double = Float64l
decimal128 = Array(16, Byte)

# Non-terminals
element = Struct(
    "type" / signed_byte,
    "name" / CString("utf8"),
    "value" / Switch(this.type, {
        1: double,
        2: Prefixed(int32, CString("utf8")),
        3: LazyBound(lambda: document),
        4: LazyBound(lambda: document),
        5: Prefixed(int32, GreedyBytes),
        6: Pass,
        7: Array(12, Byte),
        8: unsigned_byte,
        9: int64,
        10: Pass,
        11: Struct("pattern" / CString("utf8"), "options" / CString("utf8")),
        12: Struct("namespace" / CString("utf8"), "id" / Array(12, Byte)),
        13: Prefixed(int32, CString("utf8")),
        14: Prefixed(int32, CString("utf8")),
        15: Struct("code" / Prefixed(int32, CString("utf8")), "scope" / LazyBound(lambda: document)),
        16: int32,
        17: uint64,
        18: int64,
        19: decimal128,
        -1: Pass,
        127: Pass,
    })
)

e_list = GreedyRange(element)

def _calc_size(this):
    return  len(e_list.build(this["elements"]))

document = Struct(
    "size" / Rebuild(int32, _calc_size),
    "elements" / e_list
)
