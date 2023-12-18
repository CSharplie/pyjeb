# Custom variables
Use _variables_ parameter with a dictionary of scalar to add custom variables accessible with "$var.variable_name" syntax


_Exemple:_
``` python
import yaml
from pyjeb import control_and_setup

# setup control
controls = yaml.safe_load("""
- name: "favorite_color"
- name: "least_liked_color"
""")

# setup configuration
configuration = yaml.safe_load("""
    favorite_color: "$var.first_color"
    least_liked_color: "$var.second_color"
""")

# setup custom variable
custom_variables = {
    "first_color": "red",
    "second_color" : "blue"
}

# apply the control and instantiate variables
configuration = control_and_setup(configuration, controls, variables=custom_variables)

# display values 
print(f"favorite_color = '{configuration['favorite_color']}'")
print(f"least_liked_color = '{configuration['least_liked_color']}'")
```

_Output of the script_
``` ini
favorite_color = 'red'
least_liked_color = 'blue'
```

# Custom variable function
Use _functions_ parameter with a dictionary of function to add custom parametrized variables accessible with "$func.variable_name('\<parameter>')" syntax.

_:warning: custom functions are evaluated on control_and_setup call_

_:warning: custom functions can allow only one parameter_

_Exemple:_
``` python
import yaml
from pyjeb import control_and_setup

# setup control
controls = yaml.safe_load("""
- name: "favorite_color"
- name: "least_liked_color"
""")

# setup configuration
configuration = yaml.safe_load("""
    favorite_color: "$func.uppercase('Red')"
    least_liked_color: "$func.lowercase('Blue')"
""")

def uppercase_custom_func(color_name):
    return color_name.upper()

# setup custom function
custom_functions = {
    "uppercase": uppercase_custom_func, # from previous definition
    "lowercase": lambda x: x.lower() # from lambda
}

# apply the control and instantiate variables
configuration = control_and_setup(configuration, controls, functions=custom_functions)

# display values 
print(f"favorite_color = '{configuration['favorite_color']}'")
print(f"least_liked_color = '{configuration['least_liked_color']}'")
```

_Output of the script_
``` ini
favorite_color = 'RED'
least_liked_color = 'blue'
```