# Controls configuration

Control configuration is settings use to ensure the configuration file is correctly setup. It will check:
- if all mandatory nodes are existing
- if fields are setup with correct value.
- if fields are setup with correct type.

# Control types
| Name     |  Type  | Description |
|----------|:------:|-------------|
| default  | string | Default value is assigne if the node is not defined. If a default value is not defined then the node is mandatory
| regex    | string | Regex is executed to check a specific format in a code value (like email, phone number, etc.)
| validset |  list  | Validset is used to controle if a value is contains in a list
| type |  string  | The type can be specified ton control the value and the value will be cast in the target type. <br> __Available values:__ string, integer, boolean, float, list, dict  <br> __Default value:__ string

# Exemple
This exemple is an exemple (with yaml or json) of control file checking:
- if a node "path" exists
- if a node "pattern" exists. If not, assign the default value
- if a node "phone" exists and match qui provided pattern
- if a node "cold" inside a node "colurs" exists and the value is contains in the validset
- if a node "red" inside a node "colurs" exists and the value is contains in the validset

The control configuration can be developpe in serval way like:
* Yaml file
* JSON file
* Python dictonary object

## From yaml
_controls.yaml_
``` yaml
- name "path"
- name: "pattern"
  default : "*"
- name: "phone"
  regex: "[+]33[67]\d{8}"
- name: "colors.cold"
  validset:
    - "blue"
    - "green"
- name: "colors.hot"
  validset:
    - "red"
    - "yellow"
```
_exemple.py_
``` python
import yaml

# load configuration file
with open("controls.yaml") as f:
    controls = yaml.load(f, Loader = yaml.loader.SafeLoader)
```
## From json
_controls.yaml_
``` json
[
    {
        "name": "path",
    },
    {
        "name": "pattern",
        "default" : "*"
    },
    {
        "name": "phone",
        "regex": "[+]33[67]\\d{8}"
    },
    {
        "name": "colors.cold",
        "validset" : ["blue", "green"]
    },
    {
        "name": "colors.hot",
        "validset" : ["red", "yellow"]
    }
]
```
_exemple.py_
``` python
import json

# load configuration file
with open("controls.json") as f:
    controls = json.load(f)
```


## From json
_exemple.py_
``` python
controls = [
    {
        "name": "path",
    },
    {
        "name": "pattern",
        "default" : "*"
    },
    {
        "name": "phone",
        "regex": "[+]33[67]\\d{8}"
    },
    {
        "name": "colors.cold",
        "validset" : ["blue", "green"]
    },
    {
        "name": "colors.hot",
        "validset" : ["red", "yellow"]
    }
]

```