import robot.api
import construct
import io
import importlib
import re
from robot.api.deco import keyword, library
import robot.api.logger


_split_at_dot_escape_with_dotdot = re.compile(r'(?<!\.)\.(?!\.)')

@library
class robotframework_construct:
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self):
        self.constructs = {}

    @keyword('Register construct `${spec}´ from `${library}´ as `${identifier}´')
    def register_construct(self, spec: str, library: str, identifier: str):
        library = importlib.import_module(library)
        spec = getattr(library, spec)
        assert isinstance(spec, construct.Construct), f"spec should be a construct.Construct, but was {type(spec)}"
        self.constructs[identifier] = spec

    @keyword('Parse ${binarydata} using construct `${identifier}´')
    def parse_binary_data_using_construct(self, binarydata, identifier: str):
        if not isinstance(binarydata, io.BytesIO):
            try:
                binarydata = io.BytesIO(binarydata)
            except TypeError as e:
                assert False, f"could not convert {binarydata} to io.BytesIO: {e}, needs to be a byte array or a readable binary file object..."

        rVal = self.constructs[identifier].parse_stream(binarydata)
        robot.api.logger.info(f"""parsed: {rVal} using {identifier} from {binarydata}""")
        return rVal
    
    @keyword('Generate binary from ${data} using construct `{identifier}´')
    def generate_binary_data_using_construct(self, data: dict, identifier: str):
        rVal = (self.constructs[identifier].build(data))
        robot.api.logger.info(f"""built: {rVal} using `{identifier}´ from `{data}´""")
        return rVal
    
    @keyword('Elemement `${locator}´ in `${constructDict}´ should be equal to `${expectedValue}´')
    def construct_element_should_be_equal(self, locator:str, constructDict, expectedValue):
        robot.api.logger.info(repr(constructDict) + " " + str(constructDict))
        element = self._get_element_from_constructDict(constructDict, locator)
        assert element == expectedValue, f"observed value `{str(element)}´ does not match expected `{expectedValue}´ in `{str(constructDict)}´ at `{locator}´"

    @keyword('Get elemement `${locator}´ from ${constructDict}')
    def get_construct_element(self, constructDict:dict, locator:str, expectedValue):
        return self._get_element_from_constructDict(constructDict, locator)

    def _get_element_from_constructDict(self, constructDict, locator):
        assert isinstance(constructDict, dict), f"constructDict should be a dict, but was `{type(constructDict)}´"
        assert isinstance(locator, str), f"locator should be a string, but was `{type(locator)}´"
        original = constructDict
        try:
            for item in _split_at_dot_escape_with_dotdot.split(locator):
                if isinstance(constructDict, list):
                    constructDict = constructDict[int(item)]
                else:
                    constructDict = constructDict[item]
        except KeyError:
            assert False, f"could not find `{locator}´ in `{original}´"
        except TypeError as e:
            assert False, f"Cant lookup in `{type(constructDict)}´, which was encountered while looking up `{locator}´ in `{original}´ due to `{e}´"
        return constructDict
