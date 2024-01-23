"""Mains functions of PyJeb"""

import copy
import dataclasses
import json

from pyjeb.controls import cast_to_type, check_type, get_controls_of_controls, check_empty, check_validset, check_regex
from pyjeb.variables import set_variable_value
from pyjeb.exception import InvalidParameterException

@dataclasses.dataclass
class ConfigurationObject:
    """class to wrap export to oject"""

    def __init__(self, obj):
        self.__dict__.update(obj)

def get_nested_dict(config, control, controls, level = 0):
    """Get value of nested dictionary"""
    levels = control["name"].split(".")

    if isinstance(config, dict):
        level_name = levels[level]
        if level_name in config.keys():
            r = get_nested_dict(config[level_name], control, controls, level + 1)
            return r
        return None
    if isinstance(config, list):
        parent_level_name = ".".join(levels[0:level])
        level_controls = []
        for current_control in controls:
            if current_control["name"].startswith(f"{parent_level_name}."):
                level_control = copy.deepcopy(current_control)
                level_control["name"] = level_control["name"].replace(f"{parent_level_name}.", "")
                level_controls.append(level_control)

        for item in config:
            internal_control_and_setup(item, level_controls, {}, {})

        return "__is_list__"

    return config


def set_nested_dict(nested_dict, keys, new_value):
    """Set value of nested dictionary"""

    if new_value == "__is_list__":
        return

    if len(keys) == 1:
        nested_dict[keys[0]] = new_value
    else:
        key = keys[0]
        if key in nested_dict:
            set_nested_dict(nested_dict[key], keys[1:], new_value)

def internal_control_and_setup(configuration: dict, controls: list, variables: dict, functions: dict):
    """Apply controls on configuration and setup variables"""

    controls = copy.deepcopy(controls)

    for item in controls:
        if "nocheck" in item.keys() and item["nocheck"] is True:
            continue

        default_defined = "default" in item
        default_value = item["default"] if default_defined else None

        item_name = item["name"]
        is_nested = "." in item_name

        # get value from configuration node
        item_value = None
        if not is_nested and item_name in configuration.keys():
            item_value = configuration[item_name]

        if is_nested:
            levels = item_name.split(".")
            item_value = get_nested_dict(configuration, item, controls)
            if item_value == "__is_list__":
                continue

        # check empty
        if not check_empty(item_value, default_defined):
            raise InvalidParameterException(f"Property '{item_name}' can't be empty")

        # setup default value
        if item_value is None and not is_nested:
            configuration[item_name] = default_value
            item_value = default_value

        elif item_value is None and is_nested:
            set_nested_dict(configuration, levels, default_value)
            item_value = default_value

        # setup variables values
        item_value = set_variable_value(item_value, variables, functions)

        # check type and recast
        if item_value is not None and "type" in(item) and item["type"] is not None:
            if check_type(item_value, item["type"]):
                item_value = cast_to_type(item_value, item["type"])
            else:
                raise InvalidParameterException(f"Property '{item_name}' ({item['type']}) has invalid value '{item_value}'")

        # check validset value
        if "validset" in(item) and item["validset"] is not None and not check_validset(item_value, item["validset"]):
            allowed_values = "', '".join(item["validset"])
            raise InvalidParameterException(f"Property '{item_name}' ('{allowed_values}') has invalid value '{item_value}'")

        # check regex value
        if "regex" in(item) and item["regex"] is not None and not check_regex(item_value, item["regex"]):
            raise InvalidParameterException(f"Property '{item_name}' ({item['regex']}) has invalid value '{item_value}'")

        # apply new value on configuration
        if not is_nested:
            configuration[item_name] = item_value
        else:
            set_nested_dict(configuration, levels, item_value)

    return configuration

def control_and_setup(configuration: any, controls: list, variables: dict = None, functions: dict = None, to_object: bool = False):
    """Apply controls on configuration and setup variables"""

    controls = copy.deepcopy(controls)

    if controls is None:
        controls = []

    if variables is None:
        variables = {}

    if functions is None:
        functions = {}

    control_of_control = get_controls_of_controls()
    for current_control in controls:
        internal_control_and_setup(current_control, control_of_control, {}, {})

    configuration = internal_control_and_setup(configuration, controls, variables, functions)

    if to_object:
        configuration = json.loads(json.dumps(configuration), object_hook=ConfigurationObject)

    return configuration
