import robotframework_construct
import pytest


def test_impossible_params():
    with pytest.raises(AssertionError):
        robotframework_construct.robotframework_construct().traverse_construct_for_element(0, 0, 0, 0)
    
    with pytest.raises(AssertionError):
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(None, "nope")
    
    with pytest.raises(AssertionError):
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(b"", 0)
    
    with pytest.raises(AssertionError):
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(0, 0)

    with pytest.raises(AssertionError):
        robotframework_construct.robotframework_construct().construct_element_should_not_be_equal("a", {"a": [1]}, [1])

