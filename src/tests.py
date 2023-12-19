import pytest
from datetime import datetime
from pyjeb.main import control_and_setup, set_variable_value
from pyjeb.controls import check_regex, check_type, check_validset, check_empty, cast_to_type

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
    },
    {
        "name": "phone",
        "default": "+33712345678",
        "regex": "[+]33[67]\\d{8}"
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

    assert check_validset("blue", allowed_colors) == True
    assert check_validset("yellow", allowed_colors) == True
    assert check_validset("red", allowed_colors) == True
    assert check_validset("orange", allowed_colors) == False
    assert check_validset("green", allowed_colors) == False


def test_empty_control():
    with pytest.raises(ValueError) as exc_notdefault:  
        check_empty("color", None, False, "configuration")

    assert check_empty("color", "red", True, "configuration") == True
    assert str(exc_notdefault.value) == "'color' property can't be empty in configuration"

def test_regex_control():
    assert check_regex("phone", "+33712345678", "[+]33[67]\\d{8}") == True
    assert check_regex("phone", "+21698123456", "[+]33[67]\\d{8}") == False

def test_type_control():
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
        assert type(cast_to_type(test["input"], test["type_str"])) is test["type"]
        assert cast_to_type(test["input"], test["type_str"]) == test["output"]


def test_configuration_file_success():
    config_success = control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" } }, controls, variables, functions)

    assert config_success["path"] == "/root/red"
    assert config_success["colors"]["cold"] == "blue"
    assert config_success["colors"]["hot"] == "red"

def test_configuration_file_exceptions():
    with pytest.raises(ValueError) as exc_validset:  
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "yellow" } }, controls, variables, functions)
    
    with pytest.raises(ValueError) as exc_empty:  
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "hot": "red" } }, controls, variables, functions)

    assert str(exc_validset.value) == "Property 'colors.cold' ('blue', 'green') has invalid value 'yellow'"
    assert str(exc_empty.value) == "'colors.cold' property can't be empty in configuration"
