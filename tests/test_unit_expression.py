"""Test unit expression."""

from datetime import datetime
import pytest
from pyjeb.expression import apply_boolean_expression, apply_expression, get_configuration_value, get_expresion_value
from pyjeb.exception import InvalidControlException

configuration = {
    "Colors": { "cold": "blue" },
    "Count": 10,
    "Active": False,
    "Options": {
        "ignore": [
            "test 1",
            "test 2"
        ]
    },
    "useless": "cat",
    "usefull": "cat"
}

def tests_get_configuration_value():
    """Test get_configuration_value function. Ensure configuration values are retrieved correctly."""

    assert get_configuration_value("Colors.cold", configuration) == "blue"
    assert get_configuration_value("Count", configuration) == 10
    assert get_configuration_value("Active", configuration) == False
    assert get_configuration_value("useless", configuration) == "cat"

def tests_get_expresion_value():
    """Test get_expresion_value function. Ensure expression values are retrieved correctly."""

    assert get_expresion_value(configuration, "", "", "Colors.cold") == "blue"
    assert get_expresion_value(configuration, "red", "", "") == "red"
    assert get_expresion_value(configuration, "", "null", "") == None

def tests_apply_expression():
    """Test apply_expression function. Ensure expressions are evaluated correctly."""

    # compare string with string
    assert apply_expression("red", "if 'red' == 'red' return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if 'red' == 'blue' return 'blue'", configuration) == "yellow"

    # compare path with string
    assert apply_expression("yellow", "if Colors.cold == 'blue' return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if Colors.cold == 'green' return 'blue'", configuration) == "yellow"
    assert apply_expression("yellow", "if Colors.cold <> 'green' return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if Colors.cold <> 'blue' return 'blue'", configuration) == "yellow"

    # compare string with path
    assert apply_expression("yellow", "if 'blue' == Colors.cold return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if 'green' == Colors.cold return 'blue'", configuration) == "yellow"
    assert apply_expression("yellow", "if 'green' <> Colors.cold return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if 'blue' <> Colors.cold return 'blue'", configuration) == "yellow"

    # compare path with string
    assert apply_expression("yellow", "if useless == usefull return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if useless == Count return 'blue'", configuration) == "yellow"
    assert apply_expression("yellow", "if useless <> Count return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if useless <> usefull return 'blue'", configuration) == "yellow"

def test_apply_boolean_expression():
    """Test apply_boolean_expression function. Ensure boolean expressions are evaluated correctly."""

    assert apply_boolean_expression("useless == usefull", configuration) == "true"
    assert apply_boolean_expression("useless == Count", configuration) == "false"
    assert apply_boolean_expression("useless <> Count", configuration) == "true"
    assert apply_boolean_expression("useless <> usefull", configuration) == "false"

def test_apply_boolean_expression_invalid():
    """Test apply_boolean_expression function with invalid expressions. Ensure exceptions are raised."""

    with pytest.raises(InvalidControlException) as exc_info:
        apply_boolean_expression("useless = usefull", configuration)

    assert "is not a valid expression" in str(exc_info.value)
