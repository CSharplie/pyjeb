# Controls — Expressions

Expressions allow a field's value to be **overridden** based on the value of a sibling field. They are evaluated before type checking and validation.

## Syntax

```python
{ "name": "field", "expressions": ["if <left> <op> <right> return <value>"] }
```

- `<left>` and `<right>`: a quoted string (`'value'`), `null`, or a sibling field path
- `<op>`: `==` (equal) or `<>` (not equal)
- `<value>`: a quoted string, `null`, or a sibling field path

Multiple expressions are evaluated in order. The first match applies; subsequent expressions are skipped.

---

## Example: derive a value from a sibling field

Automatically set `source.pattern` based on `source.format`:

```python
{
    "name": "source.pattern",
    "default": "*",
    "expressions": [
        "if source.format == 'csv' return '*.csv'",
        "if source.format == 'json' return '*.json'",
        "if source.format == 'parquet' return '*.parquet'"
    ]
}
```

Configuration:

```yaml
ingest_orders:
  source:
    path: "/landing/prod/orders/2026-05-11"
    format: "json"
  target:
    path: "/bronze/prod/orders"
```

Result: even though `source.pattern` is not set in the file, it resolves to `"*.json"` because `source.format` is `"json"`.

---

## Example: override based on another field

Override `target.mode` when the job is disabled:

```python
{
    "name": "target.mode",
    "default": "append",
    "validset": ["append", "overwrite"],
    "expressions": ["if enabled == 'false' return 'overwrite'"]
}
```

---

## Operators

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `<>` | Not equal |

---

## Using sibling field paths as values

The return value can itself be a sibling field path:

```python
{
    "name": "target.path",
    "expressions": ["if source.path == null return source.path"]
}
```

---

## Using `null`

```python
{
    "name": "source.pattern",
    "default": "*",
    "expressions": ["if source.format == 'parquet' return null"]
}
```

Returns `None` when `source.format` is `"parquet"`.

---

## Full example

```python
import yaml
from pyjeb import control_and_setup

controls = [
    { "name": "source", "type": "dict" },
    { "name": "source.path" },
    { "name": "source.format", "validset": ["csv", "json", "parquet"] },
    {
        "name": "source.pattern",
        "default": "*",
        "expressions": [
            "if source.format == 'csv' return '*.csv'",
            "if source.format == 'json' return '*.json'",
            "if source.format == 'parquet' return '*.parquet'"
        ]
    },
    { "name": "target", "type": "dict" },
    { "name": "target.path" },
    { "name": "target.mode", "default": "append", "validset": ["append", "overwrite"] },
    { "name": "enabled", "type": "boolean", "default": True },
    { "name": "max_retries", "type": "integer", "default": 3 },
    { "name": "threshold", "type": "decimal", "default": 0.95 },
    { "name": "tags", "type": "list", "default": [] },
]

job_config = {
    "source": { "path": "/landing/prod/orders/2026-05-11", "format": "json" },
    "target": { "path": "/bronze/prod/orders" }
}

job = control_and_setup(job_config, controls, to_object=True)
print(job.source.pattern)   # *.json  (derived from source.format)
print(job.target.mode)      # append  (default)
```
