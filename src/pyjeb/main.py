from pyjeb.controls import get_controls_of_controls, check_empty, check_validset, check_regex
from pyjeb.variables import set_variable_value

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

def internal_control_and_setup(configuration: dict, controls: list = [], variables: dict = {}, functions: dict = {}, context: str = None):
    for item in controls:
        if "nocheck" in item.keys() and item["nocheck"] == True:
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
            item_value = get_nested_dict(configuration, levels, controls, item_name) 

        check_empty(item_name, item_value, default_defined, context)
        
        # setup default value
        if item_value == None and not is_nested:
            configuration[item_name] = default_value
            item_value = default_value

        elif item_value == None and is_nested:
            set_nested_dict(configuration, levels, default_value)
            item_value = default_value

        # setup variables values
        item_value = set_variable_value(item_value, variables, functions)
        if(not is_nested):
            configuration[item_name] = item_value
        else:
            set_nested_dict(configuration, levels, item_value)
    
        if "validset" in(item) and item["validset"] != None:
            check_validset(item_name, item_value, item["validset"])

        if "regex" in(item) and item["regex"] != None:
            check_regex(item_name, item_value, item["regex"])

    return configuration
    
def control_and_setup(configuration: any, controls: list = [], variables: dict = {}, functions: dict = {}):
    control_of_control = get_controls_of_controls()
    for current_control in controls:
        internal_control_and_setup(current_control, control_of_control, context="control configuration")

    return internal_control_and_setup(configuration, controls, variables, functions, context="configuration")