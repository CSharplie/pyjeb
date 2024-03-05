import pytest
from common import controls, controls_deep_array, controls_nested, variables, functions
from pyjeb.main import control_and_setup
from pyjeb.exception import InvalidTypeParameterException, InvalidValueParameterException, NotProvidedParameterException

def test_config_exceptions():
    """Test test_config_file_success with incorrect sample"""

    with pytest.raises(InvalidValueParameterException) as exc_validset:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "yellow" } }, controls, variables, functions)

    with pytest.raises(NotProvidedParameterException) as exc_empty:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "hot": "red" } }, controls, variables, functions)

    with pytest.raises(InvalidValueParameterException) as exc_regex:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "phone": "Back & Yellow" }, controls, variables, functions)

    with pytest.raises(InvalidTypeParameterException) as exc_type_int:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "count": True }, controls, variables, functions)

    with pytest.raises(InvalidTypeParameterException) as exc_type_bool:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "active": 10.5 }, controls, variables, functions)

    with pytest.raises(InvalidTypeParameterException) as exc_type_decimal:
        control_and_setup({ "path": "/root/$var.first_color", "colors": { "cold": "blue" }, "threshold": True }, controls, variables, functions)

    assert str(exc_validset.value) == "Property 'colors.cold' ('blue', 'green') has invalid value 'yellow'"
    assert str(exc_empty.value) == "The property 'colors.cold' is not setup and have no default value"
    assert str(exc_regex.value) == "Property 'phone' ([+]33[67]\\d{8}) has invalid value 'Back & Yellow'"
    assert str(exc_type_int.value) == "Property 'count' has invalid value 'True' (type must be integer)"
    assert str(exc_type_bool.value) == "Property 'active' has invalid value '10.5' (type must be boolean)"
    assert str(exc_type_decimal.value) == "Property 'threshold' has invalid value 'True' (type must be decimal)"

def test_configuration_nested_exceptions():
    """Test test_config_file_success with incorrect sample"""

    with pytest.raises(InvalidTypeParameterException) as exc_type:
        control_and_setup({
            "vehicles": {
                "cars": [
                    { "color": "red", "buy_date": "2022-05-24" },
                    { "color": "blue", "is_broken": "ok", "buy_date": "$sys.timestamp('YYYY-MM-DD')" }
                ]
            }
        }, controls_nested)

    with pytest.raises(InvalidValueParameterException) as exc_validset:
        control_and_setup({
            "vehicles": {
                "cars": [
                    { "color": "yellow", "buy_date": "2022-05-24" },
                    { "color": "blue", "is_broken": True, "buy_date": "$sys.timestamp('YYYY-MM-DD')" }
                ]
            }
        }, controls_nested)

    with pytest.raises(NotProvidedParameterException) as exc_empty:
        control_and_setup({
            "vehicles": {
                "cars": [
                    { "color": "red", "buy_date": "2022-05-24" },
                    { "color": "blue", "is_broken": True }
                ]
            }
        }, controls_nested)


    assert str(exc_validset.value) == "Property 'vehicles.cars.color' ('red', 'blue') has invalid value 'yellow'"
    assert str(exc_empty.value) == "The property 'vehicles.cars.buy_date' is not setup and have no default value"
    assert str(exc_type.value) == "Property 'vehicles.cars.is_broken' has invalid value 'ok' (type must be boolean)"



def test_configuration_deep_array_exceptions():
    """Test array inside array with incorrect sample"""

    with pytest.raises(NotProvidedParameterException) as exc_empty_level_1:
        control_and_setup({
            "workspaces": [{
                "sources": [{ "name": "test 1", "files": ["file 1", "file 2"] }]
            }]
        }, controls_deep_array)

    with pytest.raises(NotProvidedParameterException) as exc_empty_level_2:
        control_and_setup({
            "workspaces": [{
                "name": "workspace 1",
                "sources": [{ "name": "test 1" }]
            }]
        }, controls_deep_array)

    with pytest.raises(InvalidTypeParameterException) as exc_type:
        control_and_setup({
            "workspaces": [{
                "name": "workspace 1",
                "sources": [{ "name": "test 1", "files": ["file 1", "file 2"], "hidden": "yes" }]
            }]
        }, controls_deep_array)

    assert str(exc_empty_level_1.value) == "The property 'workspaces.name' is not setup and have no default value"
    assert str(exc_empty_level_2.value) == "The property 'workspaces.sources.files' is not setup and have no default value"
    assert str(exc_type.value) == "Property 'workspaces.sources.hidden' has invalid value 'yes' (type must be boolean)"
