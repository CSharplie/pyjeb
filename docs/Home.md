# PyJeb

PyJeb is a lightweight Python library to validate and variabilize configuration files.

It lets you define a **control schema** describing the expected structure of any YAML or JSON configuration, then applies it to validate values, inject defaults, and resolve variables — all in one call.

## Features

- Validate configuration structure: required fields, types, format, allowed values
- Set default values for optional fields
- Inject dynamic values: system variables, user variables, custom functions
- Case-insensitive parameter matching
- Expose configuration as an attribute-accessible Python object

## Installation

```shell
pip install pyjeb
```

## How it works

1. Write your **configuration file** (YAML or JSON)
2. Define a **control list** describing expected fields
3. Call [`control_and_setup`](api/Control-and-Setup)

## Quick Example

The following example validates and enriches data ingestion job configurations loaded from a YAML file.

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
    { "name": "threshold", "type": "decimal", "default": 0.95 },
    { "name": "tags", "type": "list", "default": [] },
]

variables = { "env": "prod" }

for job_name, job_config in config.items():
    job = control_and_setup(job_config, controls, variables=variables, to_object=True)
    print(f"{job_name}: {job.source.path}")
```

## Documentation

| Page | Description |
|---|---|
| [Getting Started](getting-started) | Step-by-step guide with a full working example |
| [control_and_setup](api/Control-and-Setup) | API reference for the main function |
| [Controls — Overview](controls/overview) | All control fields and their purpose |
| [Controls — Types](controls/types) | Supported types and type casting |
| [Controls — Validset](controls/validset) | Restrict values to an allowed set |
| [Controls — Regex](controls/regex) | Validate values against a regular expression |
| [Controls — Expressions](controls/expressions) | Conditional value mapping with expressions |
| [Controls — Conditional Controls](controls/conditional-controls) | Dynamic control rules with `if` blocks |
| [Variables — Overview](variables/overview) | Introduction to the variable system |
| [Variables — System](variables/sys-variables) | Built-in `$sys.timestamp` and `$sys.date` |
| [Variables — User](variables/user-variables) | Custom `$var.<name>` variables |
| [Variables — Functions](variables/custom-functions) | Custom `$func.<name>` functions |
| [Exceptions](exceptions) | Error types and when they are raised |
