from datetime import datetime
from pyjeb.controls import get_controls_of_controls
import re

def get_nested_dict(nested_dict, keys, controls, level):
    if type(nested_dict) is dict:
        if(keys[0] in nested_dict.keys()):
            return get_nested_dict(nested_dict[keys[0]], keys[1:], controls, level)
        else:
            return None
    elif type(nested_dict) is list:
        if len(keys) == 0:
            return "__is_list__"

        level_controls = next((x for x in controls if x["name"] == level), "default")
        level_controls["name"] = keys[0]

        for list_item in nested_dict:
            internal_control_and_setup(list_item, [level_controls])

        return "__is_list__"
    else:
        return nested_dict

def set_nested_dict(nested_dict, keys, new_value):
    if(new_value == "__is_list__"):
        return

    if len(keys) == 1:
        nested_dict[keys[0]] = new_value
    else:
        key = keys[0]
        if key in nested_dict:
            set_nested_dict(nested_dict[key], keys[1:], new_value)

def convert_timestamp_format(timestamp):
    if timestamp == "":
        return "%Y%m%d"

    timestamp = timestamp.replace("yyyy", "%Y")
    timestamp = timestamp.replace("mm", "%m")
    timestamp = timestamp.replace("dd", "%d")
    return timestamp

def set_variable_value(value, variables, functions):
    if type(value) is dict or type(value) is list or value == None:
        return value

    for match in re.findall(r"(\$(func|var|sys)\.([\w\d]+)(\('([\w\d\/\\ \-]+)'\)){0,1})", value):
        old_value, mode, name, details = match[0], match[1], match[2], match[4]
        new_value = old_value

        if mode == "sys":
            match name:
                case "timestamp":
                    format = convert_timestamp_format(details)
                    new_value = datetime.today().strftime(format)
        elif mode == "var":
            if name in variables.keys():
                new_value = variables[name]
        elif mode == "func":
            try:
                if name in functions.keys():
                    new_value = functions[name](details)
            except:
                pass

        if old_value != new_value:
            value = value.replace(old_value, new_value)

    return value    

def internal_control_and_setup(configuration: dict, controls: list = [], variables: dict = {}, functions: dict = {}, context: str = None):
    for item in controls:
        nested = "." in item["name"]

        value = None
        if(not nested and item["name"] in configuration.keys()):
            value = configuration[item["name"]]

        if(nested):
            levels = item["name"].split(".")
            value = get_nested_dict(configuration, levels, controls, item["name"]) 

        if value == None and "default" not in item:
            raise ValueError(f"'{item['name']}' property can't be empty in {context}")
        
        elif value == None and not nested:
            configuration[item["name"]] = item["default"]
            value = item["default"]

        elif value == None and nested:
            set_nested_dict(configuration, levels, item["default"])
            value = item["default"]

        value = set_variable_value(value, variables, functions)
        if(not nested):
            configuration[item["name"]] = value
        else:
            set_nested_dict(configuration, levels, value)
            
    return configuration
    


def control_and_setup(configuration: any, controls: list = [], variables: dict = {}, functions: dict = {}):
    control_of_control = get_controls_of_controls()
    for current_control in controls:
        internal_control_and_setup(current_control, control_of_control, context= "control configuration")

    return internal_control_and_setup(configuration, controls, variables, functions, context= "configuration")