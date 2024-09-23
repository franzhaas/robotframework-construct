from robot.api.deco import keyword, library
import robot.api.logger
import importlib
import construct
import collections
from dataclasses import dataclass
from robotframework_construct import _get_element_from_constructDict


@dataclass
class _regmap_entry:
    regmap: construct.Construct = None
    read_reg: callable = None
    write_reg: callable = None
    reg_size: int = -1


@library
class regmap:
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self):
        self._regmaps = collections.defaultdict(_regmap_entry)

    def _get_subcon(self, reg, identifier):
        try:
            subconNames = [i.name for i in self._regmaps[identifier].regmap.subcons]
            relevantStruct = getattr(self._regmaps[identifier].regmap, reg)
            reg = subconNames.index(reg)
        except AttributeError:
            try:
                reg = int(reg)
            except ValueError:
                assert False, f"could not find register {reg} in regmap {identifier}, neither an Integer nor a member of {", ".join(subconNames)}"
            try:
                relevantStruct = self._regmaps[identifier].regmap.subcons[reg]
            except IndexError:
                assert False, f"could not find register {reg} in regmap {identifier}, register out of bound"
        return reg,relevantStruct

    @keyword('Remove register map `${identifier}´')
    def remove_register_map(self, identifier: str):
        del self._regmaps[identifier]

    @keyword('Register regmap `${spec}´ from `${library}´ for `${identifier}´')
    def register_regmap(self, spec: str, library: str, identifier: str):
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert isinstance(spec, construct.Construct), f"spec should be a Construct, but was {type(spec)}"
        assert not isinstance(spec, construct.core.Compiled), f"spec must not be a compiled Construct, but was {type(spec)}"
        assert all(hasattr(item, "name") for item in spec.subcons), "All elements of the construct regmap need to have an identifiable name"
        assert all(item.name != "" for item in spec.subcons), "All elements of the construct regmap need to have an identifiable name"
        assert (identifier not in self._regmaps or self._regmaps[identifier].regmap is None), f"not overwriting regmap {identifier}"
        self._regmaps[identifier].regmap = spec

    @keyword('Register read register access function `${spec}´ from `${library}´ for `${identifier}´')
    def register_read_register_access_function(self, spec: str, library: str, identifier: str):
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert callable(spec), f"spec should be a callable, but was {type(spec)}"
        assert identifier not in self._regmaps or self._regmaps[identifier].read_reg is None, f"not overwriting read_reg for {identifier}"
        self._regmaps[identifier].read_reg = spec

    @keyword('Register write register access function `${spec}´ from `${library}´ for `${identifier}´')
    def register_write_register_access_function(self, spec: str, library: str, identifier: str):
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert callable(spec), f"spec should be a callable, but was {type(spec)}"
        assert identifier not in self._regmaps or self._regmaps[identifier].write_reg is None, f"not overwriting write_reg for {identifier}"
        self._regmaps[identifier].write_reg = spec

    @keyword('Read register `${reg}` from `${identifier}´')
    def read_register(self, reg, identifier: str):
        reg, relevantStruct = self._get_subcon(reg, identifier)
        regVal = self._regmaps[identifier].read_reg(reg)
        assert isinstance(regVal, bytes), f"read register should return bytes, but returned {type(regVal)}"
        if self._regmaps[identifier].reg_size != -1:
            assert len(regVal) == self._regmaps[identifier].reg_size, f"register size should remain constant but {self._regmaps[identifier].reg_size} and {len(regVal)} sizes where observed"
        self._regmaps[identifier].reg_size = len(regVal)
        return relevantStruct.parse(regVal)

    @keyword('Write register `${reg}` in `${identifier}´ with `${data}´')
    def write_register(self, reg, identifier: str, data):
        reg, relevantStruct = self._get_subcon(reg, identifier)
        if isinstance(data, bytes):
            dataOut = data
            robot.api.logger.info(f"""writing: {dataOut} using `{identifier}´ from `{data}´ unmodified""")
        else:
            try:
                dataOut = relevantStruct.build(data)
            except construct.core.ConstructError as e:
                assert False, f"could not build data with {relevantStruct} due to {e}"
            robot.api.logger.info(f"""built: {dataOut} using `{identifier}´ from `{data}´""")
        if self._regmaps[identifier].reg_size != -1:
            assert len(dataOut) == self._regmaps[identifier].reg_size, f"register size should remain constant but {self._regmaps[identifier].reg_size} and {len(dataOut)} sizes where observed"
        self._regmaps[identifier].reg_size = len(dataOut)
        return self._regmaps[identifier].write_reg(reg, dataOut)

    @keyword('Elemement `${locator}´ in `${constructDict}´ should be equal to `${expectedValue}´')
    def register_element_should_be_equal(self, locator:str, constructDict, expectedValue):
        robot.api.logger.info(repr(constructDict) + " " + str(constructDict))
        element = _get_element_from_constructDict(constructDict, locator)
        assert element == expectedValue, f"observed value `{str(element)}´ does not match expected `{expectedValue}´ in `{str(constructDict)}´ at `{locator}´"

    @keyword('Get elemement `${locator}´ from ${constructDict}')
    def get_register_element(self, locator:str, constructDict):
        return _get_element_from_constructDict(constructDict, locator)
