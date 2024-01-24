# Pyjeb

PyJeb is a powerfull lightweight library to check and variabilize your configuration files.
The main features of pyjeb are:

* Control the structure of a configuration file (missing value, type, format, valid set)
* Add default value for missing fields
* Setup variable values (system or user defined)
* Allow case insensitive parameters
* Allow to add executable functions in configuration

# Get started
## Steps
1. Install PyJeb package
2. Setup [control file](/docs/config/controls.md)
3. Setup configuration file
4. Call [control_and_setup](#setup_and_control-function) function

## Install PyJeb
Install from [PyPi](https://pypi.org/project/pyjeb/) package manager:
``` shell
pip install pyjeb
```

## Exemple
Setup a configuration file for your script. 

In this exemple a yaml file will be used, but JSON can also be used.

_Exemple of yaml configuration file - configuration.yaml_
``` yaml
HR - Employees:
  source:
    path: "/Landing/HR/Employees/$sys.timestamp('YYYY-MM-DD')"
    pattern: "*.csv"
  target:
    path: "/Bronze/HR/Employees"
HR - Managers:
  source:
    path: "/Landing/HR/Managers/$sys.timestamp('YYYY-MM-DD')"
  target:
    path: "/Bronze/HR/Managers"
HR - Payroll:
  source:
    path: "/Landing/HR/Payroll/$sys.timestamp('YYYY-MM-DD')"
  target:
    path: "/Bronze/HR/Payroll"
```

Setup a configuration to describe the previous configuration file and add default value for non mendatory field

_Exemple of yaml configuration file - control.yaml_
``` python
control = [
  { "name": "source", "type": "dict" },
  { "name": "source.path" },
  { "name": "source.pattern", "default": "*" },
  { "name": "target", "type": "dict" },
  { "name": "target.path" },
]
```

Load the configuration and apply function _control_and_setup_ function with control parameters.

This function will:
- Setup default if the value is not defined
- Setup value of variable ($sys.timestamp in this exemple)
- Set configuration as object (callable with dots)

``` python
import yaml
from pyjeb import control_and_setup

# load configuration file
with open("configuration.yaml") as f:
  configuration = yaml.load(f, Loader = yaml.loader.SafeLoader)

# control configuration
control = [
  { "name": "source", "type": "dict" },
  { "name": "source.path" },
  { "name": "source.pattern", "default": "*" },
  { "name": "target", "type": "dict" },
  { "name": "target.path" },
]

# loop on each item in configuration
for item in configuration:
  item_configuration = configuration[item]

  # apply the control and instantiate variables
  item_configuration = control_and_setup(item_configuration, control, to_object = True)

  # display values 
  print(f"--------------- {item}")
  print(f"source.path = '{item_configuration.source.path}'")
  print(f"source.pattern = '{item_configuration.source.pattern}'")
  print(f"target.path = '{item_configuration.target.path}'")

```

_Output of the script_
``` ini
--------------- HR - Employees
source.path = '/Landing/HR/Employees/2023-12-14'
source.pattern = '*.csv'
target.path = '/Bronze/HR/Employees'
--------------- HR - Managers
source.path = '/Landing/HR/Managers/2023-12-14'
source.pattern = '*'
target.path = '/Bronze/HR/Managers'
--------------- HR - Payroll
source.path = '/Landing/HR/Payroll/2023-12-14'
source.pattern = '*'
target.path = '/Bronze/HR/Payroll'
```

# setup_and_control function

The function __control_and_setup__ is the only one to use in PyJeb. It use to apply controls and setup default and variables values.

__Definition:__ control_and_setup(
    <[configuration](/docs/config/config.md)>,
    <[controls](/docs/config/controls.md)>,
    \[<[variables](/docs/variables/custom.md)>],
    \[<[functions](/docs/variables/custom.md)>]
)

| Name          | Mandatory | Type | Description |
|---------------|:---------:|:----:|:------------|
| configuration |    yes    | Dict | A dictionary (of scalar or array or dictonnary) who contain the configuration to control and variabilize
| controls      |    yes    | List | A list of dictionnaries who define the structure of configuration. See all about the structure in [controls page](/docs/config/controls.md)
| variables     |     no    | Dict | Custom variables accessible by configuration. See all about it in [custom variable page](/docs/variables/custom.md)
| functions     |     no    | Dict | Custom parametrized variables accessible by configuration. See all about it in [custom variable page](/docs/variables/custom.md)
| to_object     |     no    | Bool | Transform the output into an object. If false the output keeps dictionary format (default: false)