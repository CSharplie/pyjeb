"""Mains functions of PyJeb"""

import copy
import dataclasses
import json

from pyjeb.controls import cast_to_type, check_type, get_controls_of_controls, check_empty, check_validset, check_regex
from pyjeb.variables import set_variable_value
from pyjeb.exception import EmptyParameterException, InvalidTypeParameterException, InvalidValueParameterException, NotProvidedParameterException


@dataclasses.dataclass
class ConfigurationObject:
    """class to wrap export to oject"""

    def __init__(self, obj):
        self.__dict__.update(obj)


def internal_control_and_setup(configuration, control, variables, functions, previous = None, target_control = None):
    """Get value of nested dictionary"""

    if previous is None:
        previous = []

    # apply remaping, default values and variable setup for each dict objects
    if isinstance(configuration, dict):
        return internal_control_and_setup_dict(configuration, control, variables, functions, previous, target_control)

    # apply the logic for each item in a list exept for scalar listes
    if isinstance(configuration, list) and not all(isinstance(n, (str, int, bool, float)) for n in configuration):
        return internal_control_and_setup_list(configuration, control, variables, functions, previous, target_control)

    # skip controls if disabled
    if "nocheck" in target_control.keys() and target_control["nocheck"] is True:
        return configuration

    # apply controls on scalars values
    return internal_control_and_setup_scalar(configuration, variables, functions, target_control)


def internal_control_and_setup_dict(configuration, control, variables, functions, previous = None, target_control = None):
    """Apply remaping, default values and variable setup for each dict objects"""

    if previous == []:
        scope_controls = list(filter(lambda f: "." not in f["name"], control))
    else:
        sibling_name = ".".join(previous).upper()
        scope_controls = list(filter(lambda f: f["name"].upper().startswith(f"{sibling_name}.") and f["name"].count(".") == sibling_name.count(".") + 1, control))

    for current_control in scope_controls:
        current_full_name = current_control["name"]
        current_name = current_full_name.split(".")[-1]

        if "nocheck" in current_control.keys() and current_control["nocheck"] is True:
            continue

        # check if all target keys are setup and setup default values
        if current_name.upper() not in [item.upper() for item in configuration.keys()]:
            if "default" not in current_control.keys():
                raise NotProvidedParameterException(f"The property '{current_full_name}' is not setup and have no default value")
            configuration[current_name] = current_control["default"]

    # find all key to rename with correct case
    remap_matrix = []
    for key in configuration.keys():
        current_previous = copy.deepcopy(previous)
        current_previous.append(key)

        # pylint: disable=W0640
        target_control = list(filter(lambda f: f["name"].upper() == ".".join(current_previous).upper(), control))
        if len(target_control) == 0:
            continue

        target_control = target_control[0]
        target_name = target_control["name"].split(".")[-1]
        remap_matrix.append({ "source": key, "target": target_name })

        configuration[key] = internal_control_and_setup(configuration[key], control, variables, functions, current_previous, target_control)

    # rename source name to expected target case
    for item in remap_matrix:
        configuration[item["target"]] = configuration.pop(item["source"])

    return configuration


def internal_control_and_setup_list(configuration, control, variables, functions, previous = None, target_control = None):
    """Apply the logic for each item in a list exept for scalar listes"""
    for i, current_configuration in enumerate(configuration):
        configuration[i] = internal_control_and_setup(current_configuration, control, variables, functions, previous, target_control)
    return configuration

def internal_control_and_setup_scalar(configuration, variables, functions, target_control = None):
    """Apply controls on scalars values"""

    full_name = target_control["name"]
    have_default = "default" in target_control.keys()

    # control empty value
    if not check_empty(configuration, have_default):
        raise EmptyParameterException(f"Property '{full_name}' can't be empty")

    # setup variables values
    configuration = set_variable_value(configuration, variables, functions)

    # check type and recast
    if configuration is not None:
        if check_type(configuration, target_control["type"]):
            configuration = cast_to_type(configuration, target_control["type"])
        else:
            raise InvalidTypeParameterException(f"Property '{full_name}' has invalid value '{configuration}' (type must be {target_control['type']})")

    # check validset value
    if "validset" in(target_control.keys()) and target_control["validset"] is not None and not check_validset(configuration, target_control["validset"]):
        allowed_values = "', '".join(target_control["validset"])
        raise InvalidValueParameterException(f"Property '{full_name}' ('{allowed_values}') has invalid value '{configuration}'")

    # check regex value
    if "regex" in(target_control.keys()) and target_control["regex"] is not None and not check_regex(configuration, target_control["regex"]):
        raise InvalidValueParameterException(f"Property '{full_name}' ({target_control['regex']}) has invalid value '{configuration}'")

    return configuration

def control_and_setup(configuration: any, controls: list, variables: dict = None, functions: dict = None, to_object: bool = False):
    """Apply controls on configuration and setup variables"""

    controls = copy.deepcopy(controls)

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
