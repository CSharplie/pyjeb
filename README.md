PyJeb is a lightweight library to check and variabilize your configuration files.
The main features of pyjeb are:

* Control the structure of a configuration file
* Add default value for missing fields
* Setup variable values (system or user defined)
* Allow to add executable functions in configuration

# Get started

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