"""Function to control configuration parameters"""

import re

# control configuration for control file
def get_controls_of_controls():
    """Get the structure of control configuration"""

    return [
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "default",
            "type": "string",
            "nocheck" : True,
        },
        {
            "name": "validset",
            "type": "list",
            "default" : None,
        },
        {
            "name": "regex",
            "type": "string",
            "default" : None,
        },
        {
            "name": "type",
            "default" : "string",
            "validset" : ["string", "integer", "decimal", "boolean", "list", "dict"]
        },
    ]

def check_empty(value, default_defined):
    """Check if property is empty"""

    return not((value is None or str(value) == "")and not default_defined)

def check_validset(value, validset):
    """Check if property is include in validset"""

    return value in validset

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
            check_result = isinstance(value, list)
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
            output_value =  value
        case "dict":
            output_value =  value
        case "string":
            output_value =  value
    return output_value
