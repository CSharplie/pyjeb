"""Functions to work with PyJeb variabvles"""

import re
from datetime import datetime
from pyjeb.exception import CustomFunctionException

def convert_timestamp_format(timestamp_format):
    """Convert format from Pyjeb to Python format"""
    timestamp_format = timestamp_format.replace("YYYY", "%Y")
    timestamp_format = timestamp_format.replace("MM", "%m")
    timestamp_format = timestamp_format.replace("DD", "%d")
    timestamp_format = timestamp_format.replace("hh", "%H")
    timestamp_format = timestamp_format.replace("mm", "%M")
    timestamp_format = timestamp_format.replace("ss", "%S")

    return timestamp_format

def set_variable_value(value, variables, functions):
    """Replace the variable string by the variable value"""

    if isinstance(value, (dict, list)) or value is None:
        return value

    value = str(value)

    for match in re.findall(r"(\$(func|var|sys)\.([\w\d]+)(\('([\w\d\/\\ \-]+)'\)){0,1})", value):
        old_value, mode, name, details = match[0], match[1], match[2], match[4]
        new_value = old_value

        if mode == "sys":
            match name:
                case "timestamp":
                    if details == "":
                        details = "%Y%m%d%H%M%S"

                    timestamp_format = convert_timestamp_format(details)
                    new_value = datetime.today().strftime(timestamp_format)
                case "date":
                    if details == "":
                        details = "%Y%m%d"

                    timestamp_format = convert_timestamp_format(details)
                    new_value = datetime.today().strftime(timestamp_format)
        elif mode == "var":
            if name in variables.keys():
                new_value = str(variables[name])
        elif mode == "func":
            try:
                if name in functions.keys():
                    new_value = str(functions[name](details))
            except Exception as exc:
                raise CustomFunctionException(f"Function 'func.{name}' raise an error with parameter '{details}'") from exc

        if old_value != new_value:
            value = value.replace(old_value, new_value)

    return value
