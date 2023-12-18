import pytest
from datetime import datetime
from pyjeb.main import control_and_setup, set_variable_value
from pyjeb.controls import check_validset, check_empty

variables = {
    "first_color": "red",
    "second_color" : "blue"
}

functions = {
    "function_x10": lambda x: int(x) * 10,
    "function_x100": lambda x: int(x) * 100,
}

controls = [
    {
        "name": "path",
    },
    {
        "name": "pattern",
        "default" : "*"
    },
    {
        "name": "colors.cold",
        "validset" : ["blue", "green"]
    },
    {
        "name": "colors.hot",
        "default" : "red",
        "validset" : ["red", "yellow"]
    }
]


def tests_variable_setup():
    assert set_variable_value("$sys.date", [], [])  == datetime.today().strftime("%Y%m%d")
    assert set_variable_value("$sys.timestamp", [], [])  == datetime.today().strftime("%Y%m%d%H%M%S")
    assert set_variable_value("$sys.timestamp('YYYY-MM-DD')", [], [])  == datetime.today().strftime("%Y-%m-%d")
    assert set_variable_value("$var.first_color/$var.second_color", variables, [])  == "red/blue"
    assert set_variable_value("$func.function_x10('13')/$func.function_x100('13')", [], functions)  == "130/1300"

def test_validset_control():
    allowed_colors = ["red", "blue", "yellow"]

    with pytest.raises(ValueError) as exc_nomatch:  
        check_validset("color", "green", allowed_colors)  
    
    with pytest.raises(ValueError) as exc_badtype:  
        check_validset("color", "green", { "red" : True })  

    assert str(exc_badtype.value) == "'validset' property must be a string or array"
    assert str(exc_nomatch.value) == "'green' is not a valid value for property 'color'. The value must be one of these values: 'red', 'blue', 'yellow'"
    assert check_validset("color", "blue", allowed_colors) == True

def test_empty_control():
    with pytest.raises(ValueError) as exc_notdefault:  
        check_empty("color", None, False, "configuration")

    assert check_empty("color", "red", True, "configuration") == True
    assert str(exc_notdefault.value) == "'color' property can't be empty in configuration"

def test_configuration_file():
    with pytest.raises(ValueError) as exc_validset:  
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "yellow" } }, controls, variables, functions)
    
    with pytest.raises(ValueError) as exc_empty:  
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "hot": "red" } }, controls, variables, functions)

    config_success = control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" } }, controls, variables, functions)

    assert config_success["path"] == "/root/red"
    assert config_success["colors"]["cold"] == "blue"
    assert config_success["colors"]["hot"] == "red"

    assert str(exc_validset.value) == "'yellow' is not a valid value for property 'colors.cold'. The value must be one of these values: 'blue', 'green'"
    assert str(exc_empty.value) == "'colors.cold' property can't be empty in configuration"
