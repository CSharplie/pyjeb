# Controls — Validset

The `validset` field restricts a configuration value to a defined set of allowed values. If the value is not in the list, an `InvalidValueParameterException` is raised.

## Syntax

```python
{ "name": "source.format", "validset": ["csv", "json", "parquet"] }
```

---

## Static values

The simplest form: a list of exact allowed string values.

```python
{ "name": "source.format", "validset": ["csv", "json", "parquet"] }
{ "name": "target.mode", "default": "append", "validset": ["append", "overwrite"] }
```

**Valid** configuration:

```yaml
source:
  format: "csv"     # OK
target:
  mode: "append"    # OK
```

**Invalid** configuration:

```yaml
source:
  format: "xml"     # raises InvalidValueParameterException
```

Error message:
```
Property 'source.format' ('csv', 'json', 'parquet') has invalid value 'xml'
```

---

## Regex patterns in validset

Each entry in `validset` can also be a regex pattern. The value is tested against each entry — first as an exact match, then as a regex.

```python
{ "name": "source.path", "validset": [r"^/landing/", r"^/bronze/"] }
```

**Valid**:

```yaml
source:
  path: "/landing/prod/customers/2026-05-11"   # matches ^/landing/
```

**Invalid**:

```yaml
source:
  path: "/silver/customers"   # raises InvalidValueParameterException
```

---

## Combining static values and regex

```python
{ "name": "source.format", "validset": ["csv", "json", r"^parquet.*$"] }
```

This allows `"csv"`, `"json"`, or any string starting with `"parquet"` (e.g., `"parquet_snappy"`).

---

## Full example

```python
import yaml
from pyjeb import control_and_setup
from pyjeb.exception import InvalidValueParameterException

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

job_config = {
    "source": { "path": "/landing/prod/customers", "format": "xml" },
    "target": { "path": "/bronze/prod/customers" }
}

try:
    job = control_and_setup(job_config, controls)
except InvalidValueParameterException as e:
    print(e)
# Property 'source.format' ('csv', 'json', 'parquet') has invalid value 'xml'
```
