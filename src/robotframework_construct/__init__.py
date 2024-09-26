import robot.api
import construct
import io
import importlib
import re
from robot.api.deco import keyword, library
import robot.api.logger


class _construct_interface_basics:
    def __init__(self, element_seperator: str =r".") -> None:
        self.set_element_seperator(element_seperator)

    def _convert_to_current_type(self, expectedValue, element):
        try:
            expectedValue = type(element)(expectedValue)
        except ValueError:
            assert False, f"could not convert `{expectedValue}´ of type `{type(expectedValue)}´ to `{type(element)}´ of the original value `{element}´"
        return expectedValue

    def _get_element_from_constructDict(self, constructDict, locator):
        assert isinstance(constructDict, dict), f"constructDict should be a dict, but was `{type(constructDict)}´"
        assert isinstance(locator, str), f"locator should be a string, but was `{type(locator)}´"
        original = constructDict
        try:
            for item in self._split_at_dot_escape_with_dotdot.split(locator):
                if isinstance(constructDict, list):
                    constructDict = constructDict[int(item)]
                else:
                    constructDict = constructDict[item]
        except (KeyError, TypeError, IndexError):
            assert False, f"could not find `{locator}´ in `{original}´"
        return constructDict
    
    def _set_element_from_constructDict(self, constructDict, locator, value):
        assert isinstance(constructDict, dict), f"constructDict should be a dict, but was `{type(constructDict)}´"
        assert isinstance(locator, str), f"locator should be a string, but was `{type(locator)}´"
        original = constructDict
        try:
            element_chain = self._split_at_dot_escape_with_dotdot.split(locator)
            target = element_chain[-1]
            element_chain = element_chain[:-1]
            for item in element_chain:
                if isinstance(constructDict, list):
                    constructDict = constructDict[int(item)]
                else:
                    constructDict = constructDict[item]
            orig = getattr(constructDict, target)
        except (KeyError, AttributeError, IndexError):
            assert False, f"could not find `{locator}´ in `{original}´"
        try:
            value = type(orig)(value)
        except ValueError:
            assert False, f"could not convert `{value}´ of type `{type(value)}´ to `{type(orig)}´ of the original value `{orig}´"
        setattr(constructDict, target, value)
    
    @keyword('Set element seperator to `${element_seperator}´')
    def set_element_seperator(self, element_seperator: str):
        element_seperator = re.escape(element_seperator)
        self._split_at_dot_escape_with_dotdot = re.compile(rf'(?<!{element_seperator}){element_seperator}(?!{element_seperator})')

    @keyword('Elemement `${locator}´ in `${constructDict}´ should be equal to `${expectedValue}´')
    def construct_element_should_be_equal(self, locator:str, constructDict, expectedValue):
        element = self._get_element_from_constructDict(constructDict, locator)
        expectedValue = self._convert_to_current_type(expectedValue, element)
        assert element == expectedValue, f"observed value `{str(element)}´ does not match expected `{expectedValue}´ in `{str(constructDict)}´ at `{locator}´"

    @keyword('Elemement `${locator}´ in `${constructDict}´ should not be equal to `${expectedValue}´')
    def construct_element_should_not_be_equal(self, locator:str, constructDict, expectedValue):
        element = self._get_element_from_constructDict(constructDict, locator)
        expectedValue = self._convert_to_current_type(expectedValue, element)
        assert element != expectedValue, f"observed value `{str(element)}´ is not distinct to `{expectedValue}´ in `{str(constructDict)}´ at `{locator}´"

    @keyword('Get elemement `${locator}´ from `${constructDict}´')
    def get_construct_element(self, locator:str, constructDict:dict):
        return self._get_element_from_constructDict(constructDict, locator)
    
    @keyword('Modify the elemement located at `${locator}´ of `${constructDict}´ to `${value}´')
    def set_construct_element(self, locator:str, constructDict:dict, value):
        self._set_element_from_constructDict(constructDict, locator, value)
        return constructDict


class robotframework_construct(_construct_interface_basics):

    def __init__(self):
        self.constructs = {}
        super().__init__()

    @keyword('Register construct `${spec}´ from `${library}´ as `${identifier}´')
    def register_construct(self, spec: str, library: str, identifier: str):
        library = importlib.import_module(library)
        spec = getattr(library, spec)
        assert isinstance(spec, construct.Construct), f"spec should be a construct.Construct, but was `{type(spec)}´"
        self.constructs[identifier] = spec

    @keyword('Parse `${binarydata}´ using construct `${identifier}´')
    def parse_binary_data_using_construct(self, binarydata, identifier: str):
        if not isinstance(binarydata, io.BytesIO):
            try:
                binarydata = io.BytesIO(binarydata)
            except TypeError as e:
                assert False, f"could not convert `{binarydata}´ to io.BytesIO: `{e}´, needs to be a byte array or a readable binary file object..."

        rVal = self.constructs[identifier].parse_stream(binarydata)
        robot.api.logger.info(f"""parsed: {rVal} using {identifier} from {binarydata}""")
        return rVal
    
    @keyword('Generate binary from `${data}´ using construct `${identifier}´')
    def generate_binary_data_using_construct(self, data: dict, identifier: str):
        rVal = (self.constructs[identifier].build(data))
        robot.api.logger.info(f"""built: {rVal} using `{identifier}´ from `{data}´""")
        return rVal
