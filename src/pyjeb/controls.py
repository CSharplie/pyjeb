"""Function to control configuration parameters"""

import re

from pyjeb.exception import InvalidControlException

# control configuration for control file
def get_controls_of_controls():
    """Get the structure of control configuration"""

    return [
        # Basic controls
        {
            "name": "name",
            "type": "string",
            "expressions": [],
        },
        {
            "name": "default",
            "type": "string",
            "nocheck" : True,
            "expressions": [],
        },
        {
            "name": "validset",
            "type": "list",
            "default" : None,
            "expressions": [],
        },
        {
            "name": "regex",
            "type": "string",
            "default" : None,
            "expressions": [],
        },
        {
            "name": "type",
            "default" : "string",
            "type": "string",
            "validset" : ["string", "integer", "decimal", "boolean", "list", "dict"],
            "expressions": [],
        },
        {
            "name": "expressions",
            "type": "list",
            "default" : [],
            "expressions": [],
        },
        # Conditional controls
        {
            "name": "if",
            "type": "list",
            "default" : [],
            "expressions": [],
        },
        {
            "name": "if.expression",
            "type": "string",
            "expressions": [],
        },
        {
            "name": "if.default",
            "type": "string",
            "default" : None,
            "expressions": [],
        },
        {
            "name": "if.validset",
            "type": "list",
            "default" : None,
            "expressions": [],
        },
        {
            "name": "if.regex",
            "type": "string",
            "default" : None,
            "expressions": [],
        },
        {
            "name": "if.type",
            "type": "string",
            "default" : None,
            "validset" : ["string", "integer", "decimal", "boolean", "list", "dict"],
            "expressions": [],
        },
    ]

def check_empty(value, default_defined):
    """Check if property is empty"""

    return not((value is None or str(value) == "")and not default_defined)

def check_validset(value, validset):
    """Check if property is include in validset"""

    if value in validset:
        return True

    for regex in validset:
        try:
            if value is None or re.match(regex, value):
                return True
        except re.error:
            continue
    return False

def check_regex(value, expression):
    """Check if property match with regex"""

    return re.match(expression, value) is not None

def check_type(value, value_type):
    """Check if property type is correct"""

    check_result = False
    match value_type.lower():
        case "integer":
            check_result = re.match(r"^-{0,1} *[\d]+$", str(value)) is not None
        case "decimal":
            check_result = isinstance(value, float) or re.match(r"^-{0,1} *[\d]+(([,.])[\d]+){0,1}$", str(value)) is not None
        case "boolean":
            check_result = isinstance(value, bool) or str(value).lower() in ["true", "false"]
        case "list":
            check_result = True
        case "dict":
            check_result = isinstance(value, dict)
        case "string":
            check_result = not isinstance(value, (dict, list))
    return check_result

def cast_to_type(value, value_type):
    """Convert a value from string to the target type"""

    output_value = None
    match value_type.lower():
        case "integer":
            output_value =  int(str(value).replace(" ", ""))
        case "decimal":
            output_value =  float(str(value).replace(",", ".").replace(" ", ""))
        case "boolean":
            output_value =  str(value).lower() == "true"
        case "list":
            if isinstance(value, list):
                output_value =  value
            else:
                output_value =  [value]
        case "dict":
            output_value =  value
        case "string":
            output_value =  value
    return output_value

def check_controls_consistency(controls):
    """Check if provided controls are consistent"""
    flatten_controls = {control["name"].upper(): control["type"].lower() if "type" in control.keys() else "string" for control in controls}

    for control in controls:
        control_name = control["name"]
        if "." in control_name:
            parent_name = ".".join(control_name.split(".")[:-1])

            # Ensure that parent control is defined
            if parent_name.upper() not in flatten_controls.keys():
                raise InvalidControlException(f"The control '{control_name}' have no parent control defined")

            # Ensure that parent control is of type dict or list
            parent_type = flatten_controls[parent_name.upper()]
            if parent_type not in ["dict", "list"]:
                raise InvalidControlException(f"The control '{control_name}' have a parent control with invalid type '{parent_type}' (should be 'dict' or 'list')")
