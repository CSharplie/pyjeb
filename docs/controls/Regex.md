# Controls — Regex

The `regex` field validates a configuration value against a regular expression. The value must match the pattern for the control to pass. If it does not match, an `InvalidValueParameterException` is raised.

## Syntax

```python
{ "name": "source.path", "regex": r"^/[a-zA-Z0-9/_\$\.\-]+$" }
```

---

## Example

Validate that `source.path` starts with `/` and contains only valid path characters:

```python
{ "name": "source.path", "regex": r"^/[a-zA-Z0-9/_\$\.\-]+$" }
```

**Valid**:

```yaml
source:
  path: "/landing/prod/customers/2026-05-11"   # OK
```

**Invalid**:

```yaml
source:
  path: "landing/prod/customers"   # raises InvalidValueParameterException (no leading /)
```

Error message:
```
Property 'source.path' (^/[a-zA-Z0-9/$_\.\-]+$) has invalid value 'landing/prod/customers'
```

---

## Combined with `validset`

`regex` and `validset` can be used together on the same field. Both constraints must pass.

```python
{
    "name": "source.format",
    "validset": ["csv", "json", "parquet"],
    "regex": r"^[a-z]+$"
}
```

---

## Full example

```python
import yaml
from pyjeb import control_and_setup
from pyjeb.exception import InvalidValueParameterException

controls = [
    { "name": "source", "type": "dict" },
    { "name": "source.path", "regex": r"^/[a-zA-Z0-9/_\$\.\-]+$" },
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

job_config = {
    "source": { "path": "landing/prod/customers", "format": "csv" },
    "target": { "path": "/bronze/prod/customers" }
}

try:
    job = control_and_setup(job_config, controls)
except InvalidValueParameterException as e:
    print(e)
# Property 'source.path' (^/[a-zA-Z0-9/$_\.\-]+$) has invalid value 'landing/prod/customers'
```
