from datetime import datetime
from pyjeb.expression import apply_expression, get_configuration_value, get_expresion_value

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
    assert get_configuration_value("Colors.cold", configuration) == "blue"
    assert get_configuration_value("Count", configuration) == 10
    assert get_configuration_value("Active", configuration) == False
    assert get_configuration_value("useless", configuration) == "cat"

def tests_get_expresion_value():
    assert get_expresion_value(configuration, "", "", "Colors.cold") == "blue"
    assert get_expresion_value(configuration, "red", "", "") == "red"
    assert get_expresion_value(configuration, "", "null", "") == None

def tests_apply_expression():
    # compare string with string
    assert apply_expression("red", "if 'red' == 'red' return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if 'red' == 'blue' return 'blue'", configuration) == "yellow"
    
    # compare path with string
    assert apply_expression("yellow", "if Colors.cold == 'blue' return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if Colors.cold == 'green' return 'blue'", configuration) == "yellow"
    
    # compare string with path
    assert apply_expression("yellow", "if 'blue' == Colors.cold return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if 'green' == Colors.cold return 'blue'", configuration) == "yellow"
    
    # compare path with string
    assert apply_expression("yellow", "if useless == usefull return 'blue'", configuration) == "blue"
    assert apply_expression("yellow", "if useless == Count return 'blue'", configuration) == "yellow"


