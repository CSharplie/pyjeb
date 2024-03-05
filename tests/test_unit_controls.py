from datetime import datetime
from common import variables, functions
from pyjeb.main import set_variable_value
from pyjeb.controls import check_regex, check_type, check_validset, check_empty, cast_to_type

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