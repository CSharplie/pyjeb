from datetime import datetime
import re

def convert_timestamp_format(timestamp):
    timestamp = timestamp.replace("YYYY", "%Y")
    timestamp = timestamp.replace("MM", "%m")
    timestamp = timestamp.replace("DD", "%d")
    timestamp = timestamp.replace("hh", "%H")
    timestamp = timestamp.replace("mm", "%M")
    timestamp = timestamp.replace("ss", "%S")

    return timestamp

def set_variable_value(value, variables, functions):
    if type(value) is dict or type(value) is list or value == None:
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

                    format = convert_timestamp_format(details)
                    new_value = datetime.today().strftime(format)
                case "date":
                    if details == "":
                        details = "%Y%m%d"

                    format = convert_timestamp_format(details)
                    new_value = datetime.today().strftime(format)         
        elif mode == "var":
            if name in variables.keys():
                new_value = str(variables[name])
        elif mode == "func":
            try:
                if name in functions.keys():
                    new_value = str(functions[name](details))
            except:
                pass

        if old_value != new_value:
            value = value.replace(old_value, new_value)

    return value    