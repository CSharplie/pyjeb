# control_and_setup

```python
from pyjeb import control_and_setup
```

The main function of PyJeb. Validates a configuration dictionary against a control list, applies defaults, resolves variables, and optionally converts the result to an attribute-accessible object.

## Signature

```python
def control_and_setup(
    configuration: any,
    controls: list,
    variables: dict = None,
    functions: dict = None,
    to_object: bool = False,
    ignore_consistency: bool = False
) -> any
```

## Parameters

### `configuration`

**Type**: `dict` or `list` | **Required**: Yes

The configuration data to validate and enrich. Typically loaded from a YAML or JSON file.

```python
job_config = {
    "source": {
        "path": "/landing/$var.env/customers/$sys.timestamp('YYYY-MM-DD')",
        "format": "csv",
        "pattern": "*.csv"
    },
    "target": {
        "path": "/bronze/$var.env/customers",
        "mode": "append"
    },
    "enabled": True,
    "max_retries": 3,
    "threshold": 0.95,
    "tags": ["crm", "daily"]
}
```

---

### `controls`

**Type**: `list[dict]` | **Required**: Yes

A list of control definitions. Each entry describes one field: its name, expected type, default value, allowed values, etc.

```python
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
```

See [Controls — Overview](../controls/overview) for all supported fields.

---

### `variables`

**Type**: `dict` | **Default**: `None` (treated as `{}`)

A dictionary of named values injected into configuration strings via `$var.<name>` placeholders.

```python
variables = { "env": "prod" }
```

A configuration value containing `"/landing/$var.env/customers"` resolves to `"/landing/prod/customers"`.

See [Variables — User](../variables/user-variables).

---

### `functions`

**Type**: `dict` | **Default**: `None` (treated as `{}`)

A dictionary of named callables injected via `$func.<name>('argument')` placeholders.

```python
functions = {
    "get_bucket": lambda env: f"s3://my-bucket-{env}"
}
```

See [Variables — Functions](../variables/custom-functions).

---

### `to_object`

**Type**: `bool` | **Default**: `False`

When `True`, the returned configuration is converted to a Python object where fields are accessible via dot notation.

```python
# dict access (to_object=False, default)
job["source"]["path"]

# object access (to_object=True)
job.source.path
```

---

### `ignore_consistency`

**Type**: `bool` | **Default**: `False`

By default, PyJeb validates the control list itself before processing (checking that parent fields exist for nested paths, types are valid, etc.). Set to `True` to skip this check.

> Use with caution. Inconsistent controls may produce unexpected results.

---

## Return value

Returns the validated and enriched configuration — as a `dict` by default, or as an attribute-accessible object when `to_object=True`.

---

## Full example

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
    job = control_and_setup(
        job_config,
        controls,
        variables=variables,
        to_object=True
    )
    print(f"{job_name}: {job.source.path} → {job.target.path}")
```

---

## Errors

| Exception | Cause |
|---|---|
| `NotProvidedParameterException` | A required field (no `default`) is missing |
| `EmptyParameterException` | A field is present but empty |
| `InvalidTypeParameterException` | A field value does not match the expected type |
| `InvalidValueParameterException` | A field value is not in `validset` or fails `regex` |
| `InvalidControlException` | A control definition is malformed |
| `CustomFunctionException` | A custom function raised an exception |

See [Exceptions](../exceptions) for details.
