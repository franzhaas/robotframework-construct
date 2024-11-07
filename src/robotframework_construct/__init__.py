import robot.api
import construct
import io
import importlib
import re
from robot.api.deco import keyword
import robot.api.logger
import socket
import pathlib


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
    def parse_binary_data_using_construct(self, binarydata: bytes|io.IOBase|socket.socket, identifier: str|construct.Construct):
        match binarydata:
            case socket.socket():
                binarydata = binarydata.makefile("rb")
            case bytes():
                binarydata = io.BytesIO(binarydata)
            case io.IOBase():
                pass
            case _:
                assert False, f"binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was `{type(binarydata)}´"

        match identifier:
            case str(_):
                rVal = self.constructs[identifier].parse_stream(binarydata)
            case construct.Construct():
                rVal = identifier.parse_stream(binarydata)
            case _:
                assert False, f"identifier should be a string or a construct.Construct, but was `{type(identifier)}´"
        robot.api.logger.info(f"""parsed: {rVal} using {identifier} from {binarydata}""")
        return rVal

    @keyword('Generate binary from `${data}´ using construct `${identifier}´')
    def generate_binary_data_using_construct(self, data: dict, identifier: str|construct.Construct):
        match identifier:
            case str(_):
                rVal = (self.constructs[identifier].build(data))
            case construct.Construct():
                rVal = identifier.build(data)
        robot.api.logger.info(f"""built: {rVal} using `{identifier}´ from `{data}´""")
        return rVal

    @keyword('Write binary data generated from `${data}´ using construct `${identifier}´ to `${file}`')
    def write_binary_data_using_construct(self, data: dict, identifier: str|construct.Construct, file: io.IOBase):
        match identifier:
            case str(_):
                rVal = (self.constructs[identifier].build(data))
            case construct.Construct():
                rVal = identifier.build(data)
        robot.api.logger.info(f"""built: {rVal} using `{identifier}´ from `{data}´""")
        match file:
            case io.IOBase():
                file.write(rVal)
            case socket.socket():
                file.send(rVal)

    @keyword('Open `${filepath}´ for reading binary data')
    def open_binary_file_to_read(self, filepath: str|pathlib.Path):
        return open(filepath, "rb")

    @keyword('Open `${filepath}´ for writing binary data')
    def open_binary_file_to_write(self, filepath: str|pathlib.Path):
        return open(filepath, "wb")

    @keyword('Open ${protocol} connection to server `${server}´ on port `${port}´')
    def open_socket(self, protocol: str, server:str, port:int):
        match protocol:
            case "TCP":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((server, port))
                return s
            case "UDP":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((server, port))
                return s
            case _:
                assert False, f"protocol should be either `TCP or `UDP´, but was `{protocol}´"
