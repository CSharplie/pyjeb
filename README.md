# Pyjeb

PyJeb is a lightweight library to check and variabilize your configuration files.
The main features of pyjeb are:

* Control the structure of a configuration file
* Add default value for missing fields
* Setup variable values (system or user defined)
* Allow to add executable functions in configuration

# Get started
## Steps
1. Install PyJeb package
2. Setup [control file](/docs/config/controls.md)
3. Setup [configuration file](/docs/config/config.md)
4. Call [control_and_setup](#setup_and_control-function) function

## Install PyJeb
Install from [PyPi](https://pypi.org/project/pyjeb/) package manager:
``` shell
pip install pyjeb
```

## Exemple
Setup a configuration file for your script

_Exemple of yaml configuration file - configuration.yaml_
``` yaml
HR - Employees:
  source:
    path: "/Landing/HR/Employees/$sys.timestamp('yyyy-mm-dd')"
    pattern: "*.csv"
  target:
    path: "/Bronze/HR/Employees"
HR - Managers:
  source:
    path: "/Landing/HR/Managers/$sys.timestamp('yyyy-mm-dd')"
  target:
    path: "/Bronze/HR/Managers"
HR - Payroll:
  source:
    path: "/Landing/HR/Payroll/$sys.timestamp('yyyy-mm-dd')"
  target:
    path: "/Bronze/HR/Payroll"
```

Setup a second file to describe preivous configuration file and add default value for non mendatory field

_Exemple of yaml configuration file - control.yaml_
``` yaml
- name: "source"
- name: "source.path"
- name: "source.pattern"
  default: "*"
- name: "target"
- name: "target.path"
```

Load both file and apply function _control_and_setup_ function.
This function will:
- Setup default if the value is not defined
- Setup value of variable ($sys.timestamp in this exemple)

``` python
import yaml
from pyjeb import control_and_setup

# load configuration file
with open("configuration.yaml") as f:
    configuration = yaml.load(f, Loader = yaml.loader.SafeLoader)

# load control file
with open("control.yaml") as f:
    control = yaml.load(f, Loader = yaml.loader.SafeLoader)

# loop on each item in configuration
for item in configuration:
    item_configuration = configuration[item]

    # apply the control and instantiate variables
    item_configuration = control_and_setup(item_configuration, control)

    # display values 
    print(f"--------------- {item}")
    print(f"source.path = '{item_configuration['source']['path']}'")
    print(f"source.pattern = '{item_configuration['source']['pattern']}'")
    print(f"target.path = '{item_configuration['target']['path']}'")

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