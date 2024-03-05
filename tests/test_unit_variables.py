from datetime import datetime
from common import variables, functions
from pyjeb.variables import set_variable_value

def tests_variable_setup():
    """Test set_variable_value function. Ensure the sys/var/func is assigned"""

    assert set_variable_value("$sys.date", [], [])  == datetime.today().strftime("%Y%m%d")
    assert set_variable_value("$sys.timestamp", [], [])  == datetime.today().strftime("%Y%m%d%H%M%S")
    assert set_variable_value("$sys.timestamp('YYYY-MM-DD')", [], [])  == datetime.today().strftime("%Y-%m-%d")
    assert set_variable_value("$var.first_color/$var.second_color", variables, [])  == "red/blue"
    assert set_variable_value("$func.function_x10('13')/$func.function_x100('13')", [], functions)  == "130/1300"
