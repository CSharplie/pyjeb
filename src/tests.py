"""Execute unit testing"""

from datetime import datetime
import pytest
from pyjeb.main import control_and_setup, set_variable_value
from pyjeb.controls import check_regex, check_type, check_validset, check_empty, cast_to_type
from pyjeb.exception import InvalidTypeParameterException, InvalidValueParameterException, NotProvidedParameterException

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
        "type": "string"
    },
    {
        "name": "pattern",
        "type": "string",
        "default" : "*",
    },
    {
        "name": "colors",
        "type": "dict",
    },
    {
        "name": "colors.cold",
        "type": "string",
        "validset" : ["blue", "green"]
    },
    {
        "name": "colors.hot",
        "type": "string",
        "default" : "red",
        "validset" : ["red", "yellow"]
    },
    {
        "name": "phone",
        "type": "string",
        "default": "+33712345678",
        "regex": "[+]33[67]\\d{8}"
    },
    {
        "name": "count",
        "type": "integer",
        "default" : 0
    },
    {
        "name": "threshold",
        "type": "decimal",
        "default" : 0.90
    },
    {
        "name": "active",
        "type": "boolean",
        "default" : True
    },
    {
        "name": "options",
        "type": "dict",
        "default" : {}
    },
    {
        "name": "options.ignore",
        "type": "list",
        "default" : []
    }
]

controls_nested = [
    { "name": "vehicles", "type": "dict" },
    { "name": "vehicles.cars", "type": "list" },
    { "name": "vehicles.cars.color", "validset": ["red", "blue"] },
    { "name": "vehicles.cars.is_broken", "type": "boolean", "default": False },
    { "name": "vehicles.cars.buy_date" }
]

controls_deep_array = [
    { "name": "workspaces", "type": "dict" },
    { "name": "workspaces.name", "type": "string" },
    { "name": "workspaces.sources", "type": "list" },
    { "name": "workspaces.sources.hidden", "type": "boolean", "default": False },
    { "name": "workspaces.sources.name", "type": "string"},
    { "name": "workspaces.sources.files", "type": "list"},
]

def tests_variable_setup():
    """Test set_variable_value function. Ensure the sys/var/func is assigned"""

    assert set_variable_value("$sys.date", [], [])  == datetime.today().strftime("%Y%m%d")
    assert set_variable_value("$sys.timestamp", [], [])  == datetime.today().strftime("%Y%m%d%H%M%S")
    assert set_variable_value("$sys.timestamp('YYYY-MM-DD')", [], [])  == datetime.today().strftime("%Y-%m-%d")
    assert set_variable_value("$var.first_color/$var.second_color", variables, [])  == "red/blue"
    assert set_variable_value("$func.function_x10('13')/$func.function_x100('13')", [], functions)  == "130/1300"

def test_validset_control():
    """Test check_validset function. Ensure validset control is working"""

    allowed_colors = ["red", "blue", "yellow"]

    assert check_validset("blue", allowed_colors) is True
    assert check_validset("yellow", allowed_colors) is True
    assert check_validset("red", allowed_colors) is True
    assert check_validset("orange", allowed_colors) is False
    assert check_validset("green", allowed_colors) is False


def test_empty_control():
    """Test check_empty function. Ensure empty control is working"""

    assert check_empty("red", True) is True
    assert check_empty("", True) is True
    assert check_empty(None, True) is True
    assert check_empty("red", False) is True
    assert check_empty("", False) is False
    assert check_empty(None, False) is False

def test_regex_control():
    """Test regex_control function. Ensure regex control is working"""

    assert check_regex("+33712345678", "[+]33[67]\\d{8}") is True
    assert check_regex("+21698123456", "[+]33[67]\\d{8}") is False

def test_type_control():
    """Test type_control function. Ensure type control is working"""

    test_matrice = [
            { "value": "ABC"            , "types": { "integer":False, "decimal":False   , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": -10              , "types": { "integer":True , "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": 10               , "types": { "integer":True , "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": "10"             , "types": { "integer":True , "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": "-10"            , "types": { "integer":True , "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": -10.5            , "types": { "integer":False, "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": 10.5             , "types": { "integer":False, "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": "10.5"           , "types": { "integer":False, "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": "-10.5"          , "types": { "integer":False, "decimal":True    , "boolean":False   , "list":False  , "dict":False  , "string": True }}
        ,   { "value": True             , "types": { "integer":False, "decimal":False   , "boolean":True    , "list":False  , "dict":False  , "string": True }}
        ,   { "value": False            , "types": { "integer":False, "decimal":False   , "boolean":True    , "list":False  , "dict":False  , "string": True }}
        ,   { "value": "True"           , "types": { "integer":False, "decimal":False   , "boolean":True    , "list":False  , "dict":False  , "string": True }}
        ,   { "value": "False"          , "types": { "integer":False, "decimal":False   , "boolean":True    , "list":False  , "dict":False  , "string": True }}
        ,   { "value": ["Red", "Blue"]  , "types": { "integer":False, "decimal":False   , "boolean":False   , "list":True   , "dict":False  , "string": False }}
        ,   { "value": { "Type": "Py"}  , "types": { "integer":False, "decimal":False   , "boolean":False   , "list":False  , "dict":True   , "string": False }}
    ]

    for test in test_matrice:
        assert check_type(test["value"], "integer") == test["types"]["integer"]
        assert check_type(test["value"], "decimal") == test["types"]["decimal"]
        assert check_type(test["value"], "boolean") == test["types"]["boolean"]
        assert check_type(test["value"], "list") == test["types"]["list"]
        assert check_type(test["value"], "dict") == test["types"]["dict"]
        assert check_type(test["value"], "string") == test["types"]["string"]

def test_cast_to_type():
    """Test cast_to_type function. Ensure type convertion is working"""

    test_matrice = [
        # integer
          { "input":"10"        , "output":10       , "type_str":"integer"  , "type":int}
        , { "input":10          , "output":10       , "type_str":"integer"  , "type":int}
        , { "input":"-10"       , "output":-10      , "type_str":"integer"  , "type":int}
        , { "input":-10         , "output":-10      , "type_str":"integer"  , "type":int}
        , { "input":"- 10"      , "output":-10      , "type_str":"integer"  , "type":int}
        , { "input":" 10 "      , "output":10       , "type_str":"integer"  , "type":int}
        # decimal
        , { "input":"10.5"      , "output":10.5     , "type_str":"decimal"  , "type":float}
        , { "input":"10,5"      , "output":10.5     , "type_str":"decimal"  , "type":float}
        , { "input":10.5        , "output":10.5     , "type_str":"decimal"  , "type":float}
        , { "input":"-10.5"     , "output":-10.5    , "type_str":"decimal"  , "type":float}
        , { "input":"-10,5"     , "output":-10.5    , "type_str":"decimal"  , "type":float}
        , { "input":-10.5       , "output":-10.5    , "type_str":"decimal"  , "type":float}
        , { "input":"- 10.5"    , "output":-10.5    , "type_str":"decimal"  , "type":float}
        , { "input":"- 10,5"    , "output":-10.5    , "type_str":"decimal"  , "type":float}
        , { "input":" 10.5 "    , "output":10.5     , "type_str":"decimal"  , "type":float}
        , { "input":" 10,5 "    , "output":10.5     , "type_str":"decimal"  , "type":float}
        # boolean
        , { "input":"True"      , "output":True     , "type_str":"boolean"  , "type":bool}
        , { "input":"False"     , "output":False    , "type_str":"boolean"  , "type":bool}
        , { "input":True        , "output":True     , "type_str":"boolean"  , "type":bool}
        , { "input":False       , "output":False    , "type_str":"boolean"  , "type":bool}
        # string
        , { "input":"ABC"       , "output":"ABC"    , "type_str":"string"   , "type":str}
        # list
        , { "input":["Red", "Blue"], "output":["Red", "Blue"], "type_str":"list", "type":list}
        # dict
        , { "input":{ "Type": "Py"}, "output":{ "Type": "Py"}, "type_str":"dict", "type":dict}
    ]

    for test in test_matrice:
        assert isinstance(cast_to_type(test["input"], test["type_str"]), test["type"])
        assert cast_to_type(test["input"], test["type_str"]) == test["output"]

def test_configuration_file_success():
    """Test test_configuration_file_success with correct sample"""

    configuration = {
        "Path": "/root/$var.first_color",
        "Colors": { "cold": "blue" },
        "Count": 10,
        "Active": False, 
        "Options": {
            "ignore": [
                "test 1",
                "test 2"
            ]
        },
        "useless": "cat"
    }

    config_success = control_and_setup(configuration, controls, variables, functions)
    config_success_obj = control_and_setup(configuration, controls, variables, functions, to_object=True)

    assert config_success["path"] == "/root/red"
    assert config_success["colors"]["cold"] == "blue"
    assert config_success["colors"]["hot"] == "red"
    assert config_success["count"] == 10
    assert config_success["active"] is False
    assert config_success["threshold"] == 0.9
    assert config_success["options"]["ignore"] == ["test 1", "test 2"]

    assert config_success_obj.path == "/root/red"
    assert config_success_obj.colors.cold == "blue"
    assert config_success_obj.colors.hot == "red"
    assert config_success_obj.count == 10
    assert config_success_obj.active is False
    assert config_success_obj.threshold == 0.9
    assert config_success_obj.options.ignore == ["test 1", "test 2"]

def test_configuration_file_exceptions():
    """Test test_configuration_file_success with incorrect sample"""

    with pytest.raises(InvalidValueParameterException) as exc_validset:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "yellow" } }, controls, variables, functions)

    with pytest.raises(NotProvidedParameterException) as exc_empty:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "hot": "red" } }, controls, variables, functions)

    with pytest.raises(InvalidValueParameterException) as exc_regex:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "phone": "Back & Yellow" }, controls, variables, functions)

    with pytest.raises(InvalidTypeParameterException) as exc_type_int:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "count": True }, controls, variables, functions)

    with pytest.raises(InvalidTypeParameterException) as exc_type_bool:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "active": 10.5 }, controls, variables, functions)

    with pytest.raises(InvalidTypeParameterException) as exc_type_decimal:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "threshold": True }, controls, variables, functions)

    assert str(exc_validset.value) == "Property 'colors.cold' ('blue', 'green') has invalid value 'yellow'"
    assert str(exc_empty.value) == "The property 'colors.cold' is not setup and have no default value"
    assert str(exc_regex.value) == "Property 'phone' ([+]33[67]\\d{8}) has invalid value 'Back & Yellow'"
    assert str(exc_type_int.value) == "Property 'count' has invalid value 'True' (type must be integer)"
    assert str(exc_type_bool.value) == "Property 'active' has invalid value '10.5' (type must be boolean)"
    assert str(exc_type_decimal.value) == "Property 'threshold' has invalid value 'True' (type must be decimal)"


def test_nested_configuration_file_success():
    """Test test_configuration_file_success with correct sample"""

    configuration = {
        "vehicles": {
            "cars": [
                { "color": "red", "buy_date": "2022-05-24" },
                { "color": "blue", "is_broken": True, "buy_date": "$sys.timestamp('YYYY-MM-DD')" }
            ]
        }
    }

    config_success = control_and_setup(configuration, controls_nested)
    config_success_obj = control_and_setup(configuration, controls_nested, to_object=True)

    assert config_success["vehicles"]["cars"][1]["buy_date"] == datetime.today().strftime("%Y-%m-%d")
    assert config_success["vehicles"]["cars"][0]["is_broken"] is False

    assert config_success_obj.vehicles.cars[1].buy_date == datetime.today().strftime("%Y-%m-%d")
    assert config_success_obj.vehicles.cars[0].is_broken is False

def test_nested_configuration_file_exceptions():
    """Test test_configuration_file_success with incorrect sample"""

    with pytest.raises(InvalidTypeParameterException) as exc_type:
        control_and_setup({
            "vehicles": {
                "cars": [
                    { "color": "red", "buy_date": "2022-05-24" },
                    { "color": "blue", "is_broken": "ok", "buy_date": "$sys.timestamp('YYYY-MM-DD')" }
                ]
            }
        }, controls_nested)

    with pytest.raises(InvalidValueParameterException) as exc_validset:
        control_and_setup({
            "vehicles": {
                "cars": [
                    { "color": "yellow", "buy_date": "2022-05-24" },
                    { "color": "blue", "is_broken": True, "buy_date": "$sys.timestamp('YYYY-MM-DD')" }
                ]
            }
        }, controls_nested)

    with pytest.raises(NotProvidedParameterException) as exc_empty:
        control_and_setup({
            "vehicles": {
                "cars": [
                    { "color": "red", "buy_date": "2022-05-24" },
                    { "color": "blue", "is_broken": True }
                ]
            }
        }, controls_nested)


    assert str(exc_validset.value) == "Property 'vehicles.cars.color' ('red', 'blue') has invalid value 'yellow'"
    assert str(exc_empty.value) == "The property 'vehicles.cars.buy_date' is not setup and have no default value"
    assert str(exc_type.value) == "Property 'vehicles.cars.is_broken' has invalid value 'ok' (type must be boolean)"

def test_deep_array_configuration_file_success():
    """Test array inside array with correct sample"""

    configuration = {
        "workspaces": [
            {
                "name": "Workspace 1",
                "sources": [
                    { "name": "test 1", "files": ["file 1", "file 2"] }
                ]
            },
            {
                "name": "Workspace 2",
                "sources": [
                    { "name": "test 2", "files": ["file 3", "file 4"], "hidden": True },
                    { "name": "test 3", "files": ["file 5", "file 6"] }
                ]
            }
        ]
    }

    config_success = control_and_setup(configuration, controls_deep_array)
    config_success_obj = control_and_setup(configuration, controls_deep_array, to_object=True)

    assert config_success["workspaces"][0]["sources"][0]["hidden"] is False
    assert config_success["workspaces"][1]["sources"][0]["hidden"] is True

    assert config_success_obj.workspaces[0].sources[0].hidden is False
    assert config_success_obj.workspaces[1].sources[0].hidden is True

def test_deep_array_configuration_file_exceptions():
    """Test array inside array with incorrect sample"""

    with pytest.raises(NotProvidedParameterException) as exc_empty_level_1:
        control_and_setup({
            "workspaces": [{
                "sources": [{ "name": "test 1", "files": ["file 1", "file 2"] }]
            }]
        }, controls_deep_array)

    with pytest.raises(NotProvidedParameterException) as exc_empty_level_2:
        control_and_setup({
            "workspaces": [{
                "name": "workspace 1",
                "sources": [{ "name": "test 1" }]
            }]
        }, controls_deep_array)

    with pytest.raises(InvalidTypeParameterException) as exc_type:
        control_and_setup({
            "workspaces": [{
                "name": "workspace 1",
                "sources": [{ "name": "test 1", "files": ["file 1", "file 2"], "hidden": "yes" }]
            }]
        }, controls_deep_array)

    assert str(exc_empty_level_1.value) == "The property 'workspaces.name' is not setup and have no default value"
    assert str(exc_empty_level_2.value) == "The property 'workspaces.sources.files' is not setup and have no default value"
    assert str(exc_type.value) == "Property 'workspaces.sources.hidden' has invalid value 'yes' (type must be boolean)"
