"""Test configuration success."""

from datetime import datetime
from common import controls, controls_deep_array, controls_nested, variables, functions
from pyjeb.main import control_and_setup

def test_config_success():
    """Test test_config_file_success with correct sample"""

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

def test_configuration_nested_success():
    """Test test_config_file_success with correct sample"""

    configuration = {
        "vehicles": {
            "cars": [
                { "color": "red", "buy_date": "2022-05-24" },
                { "color": "blue", "is_broken": True, "buy_date": "$sys.timestamp('YYYY-MM-DD')" },
                { "color": "#FFFFFF", "buy_date": "2024-06-16" },
            ]
        }
    }

    config_success = control_and_setup(configuration, controls_nested)
    config_success_obj = control_and_setup(configuration, controls_nested, to_object=True)

    assert config_success["vehicles"]["cars"][0]["is_broken"] is False
    assert config_success["vehicles"]["cars"][1]["buy_date"] == datetime.today().strftime("%Y-%m-%d")
    assert config_success["vehicles"]["cars"][0]["type"] == "sportive"
    assert config_success["vehicles"]["cars"][1]["type"] == "usual"

    assert config_success_obj.vehicles.cars[0].is_broken is False
    assert config_success_obj.vehicles.cars[1].buy_date == datetime.today().strftime("%Y-%m-%d")
    assert config_success_obj.vehicles.cars[0].type == "sportive"
    assert config_success_obj.vehicles.cars[1].type == "usual"

def test_configuration_deep_array_success():
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

def test_configuration_conditional_controls_success():
    """Test conditional controls with dynamic default, type, validset and regex."""

    conditional_controls = [
        {
            "name": "fields",
            "type": "list",
            "default": []
        },
        {
            "name": "fields.name"
        },
        {
            "name": "fields.type",
            "validset": ["boolean", "number", "string"]
        },
        {
            "name": "fields.format_default",
            "type": "integer",
            "if": [
                {
                    "expression": "type == 'number'",
                    "default": "2",
                    "type": "string"
                },
                {
                    "expression": "type <> 'number'",
                    "default": "none",
                    "type": "string"
                }
            ]
        },
        {
            "name": "fields.format_rules",
            "type": "integer",
            "if": [
                {
                    "expression": "type == 'number'",
                    "type": "string",
                    "validset": ["^[0-9]+$"],
                    "regex": "^[0-9]{1}$"
                },
                {
                    "expression": "type <> 'number'",
                    "type": "string",
                    "validset": ["^[a-z0-9-]+$"],
                    "regex": "^[a-z]+$"
                }
            ]
        },
        {
            "name": "fields.mode",
            "type": "integer",
            "if": [
                {
                    "expression": "type == 'number'",
                    "type": "string",
                    "default": "fixed",
                    "validset": ["fixed", "dynamic"]
                },
                {
                    "expression": "type <> 'number'",
                    "type": "string",
                    "default": "none",
                    "validset": ["none", "auto"]
                }
            ]
        },
        {
            "name": "fields.mode_rules",
            "type": "integer",
            "if": [
                {
                    "expression": "type == 'number'",
                    "type": "string",
                    "validset": ["fixed", "dynamic"]
                },
                {
                    "expression": "type <> 'number'",
                    "type": "string",
                    "validset": ["none", "auto"]
                }
            ]
        }
    ]

    configuration = {
        "fields": [
            {"name": "price", "type": "number", "format_rules": "4", "mode_rules": "fixed"},
            {"name": "quantity", "type": "number", "format_rules": "7", "mode_rules": "dynamic"},
            {"name": "is_active", "type": "boolean", "format_rules": "alpha", "mode_rules": "none"},
            {"name": "label", "type": "string", "format_rules": "beta", "mode_rules": "auto"}
        ]
    }

    config_success = control_and_setup(configuration, conditional_controls)

    assert config_success["fields"][0]["format_default"] == "2"
    assert config_success["fields"][1]["format_default"] == "2"
    assert config_success["fields"][2]["format_default"] == "none"
    assert config_success["fields"][3]["format_default"] == "none"

    assert config_success["fields"][0]["format_rules"] == "4"
    assert config_success["fields"][1]["format_rules"] == "7"
    assert config_success["fields"][2]["format_rules"] == "alpha"
    assert config_success["fields"][3]["format_rules"] == "beta"

    assert config_success["fields"][0]["mode"] == "fixed"
    assert config_success["fields"][1]["mode"] == "fixed"
    assert config_success["fields"][2]["mode"] == "none"
    assert config_success["fields"][3]["mode"] == "none"

    assert config_success["fields"][0]["mode_rules"] == "fixed"
    assert config_success["fields"][1]["mode_rules"] == "dynamic"
    assert config_success["fields"][2]["mode_rules"] == "none"
    assert config_success["fields"][3]["mode_rules"] == "auto"

    assert isinstance(config_success["fields"][0]["format_default"], str)
    assert isinstance(config_success["fields"][1]["format_default"], str)
    assert isinstance(config_success["fields"][2]["format_default"], str)
    assert isinstance(config_success["fields"][3]["format_default"], str)
