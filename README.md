# PyJeb

PyJeb is a lightweight Python library to validate and variabilize your configuration files.

- Validate configuration structure: required fields, types, format, allowed values
- Set default values for optional fields
- Inject dynamic values: system variables, user variables, custom functions
- Case-insensitive parameter matching
- Expose configuration as an attribute-accessible Python object

## Installation

```shell
pip install pyjeb
```

## Quick example

_job.yaml_
```yaml
ingest_customers:
  source:
    path: "/landing/$var.env/customers/$sys.timestamp('YYYY-MM-DD')"
    format: "csv"
  target:
    path: "/bronze/$var.env/customers"

ingest_orders:
  source:
    path: "/landing/$var.env/orders/$sys.timestamp('YYYY-MM-DD')"
    format: "json"
  target:
    path: "/bronze/$var.env/orders"
```

```python
import yaml
from pyjeb import control_and_setup

with open("job.yaml") as f:
    config = yaml.safe_load(f)

controls = [
    { "name": "source", "type": "dict" },
    { "name": "source.path" },
    { "name": "source.format", "validset": ["csv", "json", "parquet"] },
    { "name": "source.pattern", "default": "*" },
    { "name": "target", "type": "dict" },
    { "name": "target.path" },
    { "name": "target.mode", "default": "append", "validset": ["append", "overwrite"] },
    { "name": "enabled", "type": "boolean", "default": True },
    { "name": "max_retries", "type": "integer", "default": 3 },
]

variables = { "env": "prod" }

for job_name, job_config in config.items():
    job = control_and_setup(job_config, controls, variables=variables, to_object=True)
    print(f"{job_name}: {job.source.path} → {job.target.path}")
```

Output (run on 2026-05-11):
```
ingest_customers: /landing/prod/customers/2026-05-11 → /bronze/prod/customers
ingest_orders: /landing/prod/orders/2026-05-11 → /bronze/prod/orders
```

## Documentation

Full documentation is available on the [GitHub wiki](https://github.com/CSharplie/pyjeb/wiki).

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

# control_and_setup function

The function __control_and_setup__ is the only one to use in PyJeb. It use to apply controls and setup default and variables values.

See all about the structure in [control_and_setup](https://github.com/CSharplie/pyjeb/wiki/control_and_setup)

# Configuration
The configuration is a dictionary of dictionaries. Each key is a section and each section is a dictionary of key-value pairs.

__Exemple:__
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

# Controls
The controls are a list of dictionaries. Each dictionary is a control to apply on the configuration.

See all about the structure in [controls page](https://github.com/CSharplie/pyjeb/wiki/controls-configuration)
