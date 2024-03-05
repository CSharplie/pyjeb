""" function to process expression on configuration"""

import re
from pyjeb.exception import InvalidControlException

def get_configuration_value(path, configuration, full_path = None):
    """Get the value of configuration of a specified path"""

    full_path = path if full_path is None else full_path
    nodes = path.split(".")
    current_node = nodes[0]
    next_path = None if len(nodes) == 1 else ".".join(nodes[1:len(nodes)])

    if current_node not in configuration.keys():
        raise InvalidControlException(f"Path '{full_path}' do not exists")

    if next_path is None:
        return configuration[current_node]

    return get_configuration_value(next_path, configuration[current_node], full_path)

def get_expresion_value(context, value, null, path):
    """Return the first value between value, null and path. And evaluate the path value"""

    if null == "null":
        return None
    if path != "":
        return get_configuration_value(path, context)

    return value

def apply_expression(value, expression, context):
    """Process the provided expression"""

    replace_value_matches = re.findall(r"^ *if *('(.*)'|(null)|([\w\d_\.]+)) *== *('(.*)'|(null)|([\w\d_\.]+)) *return *('(.*)'|(null)|([\w\d_\.]+)) *$", expression)

    if len(replace_value_matches) == 1:
        match = replace_value_matches[0]

        value_from, value_compare, value_return = match[1], match[5], match[9]
        null_from, null_compare, null_return = match[2], match[6], match[10]
        path_from, path_compare, path_return = match[3], match[7], match[11]

        expression_from = get_expresion_value(context, value_from, null_from, path_from)
        expression_compare = get_expresion_value(context, value_compare, null_compare, path_compare)
        expression_return = get_expresion_value(context, value_return, null_return, path_return)

        if expression_from == expression_compare:
            return expression_return

        return value

    raise InvalidControlException(f"The expression '{expression}' is not a valid expression")
