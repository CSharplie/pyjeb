# Controls — Conditional Controls

The `if` field allows a control's `default`, `type`, `validset`, or `regex` to change dynamically based on sibling field values. This is useful when the rules for a field depend on the value of another field.

## Syntax

```python
{
    "name": "field",
    "if": [
        {
            "expression": "<left> <op> <right>",
            "default": "...",      # optional
            "type": "...",         # optional
            "validset": [...],     # optional
            "regex": "..."         # optional
        }
    ]
}
```

Conditions are evaluated in order. The first matching condition applies its overrides to the control. The expression syntax uses the same operators as [Expressions](expressions): `==` (equal) and `<>` (not equal).

---

## Example: conditional default

Provide a different default for `source.pattern` based on the file format:

```python
{
    "name": "source.pattern",
    "if": [
        { "expression": "format == 'csv'",     "default": "*.csv" },
        { "expression": "format == 'json'",    "default": "*.json" },
        { "expression": "format == 'parquet'", "default": "*.parquet" }
    ]
}
```

Configuration:

```yaml
ingest_customers:
  source:
    path: "/landing/prod/customers/2026-05-11"
    format: "csv"
  target:
    path: "/bronze/prod/customers"
```

Result: `source.pattern` defaults to `"*.csv"` because `format` is `"csv"`.

---

## Example: conditional validset

Restrict `target.mode` to `"overwrite"` only when the format is `"parquet"`:

```python
{
    "name": "target.mode",
    "if": [
        {
            "expression": "source.format == 'parquet'",
            "validset": ["overwrite"],
            "default": "overwrite"
        },
        {
            "expression": "source.format <> 'parquet'",
            "validset": ["append", "overwrite"],
            "default": "append"
        }
    ]
}
```

---

## Example: conditional type and regex

```python
{
    "name": "max_retries",
    "if": [
        {
            "expression": "enabled == 'true'",
            "type": "integer",
            "regex": r"^[1-9][0-9]*$"
        },
        {
            "expression": "enabled == 'false'",
            "type": "string",
            "default": "0"
        }
    ]
}
```

When `enabled` is `true`, `max_retries` must be a positive integer. When `enabled` is `false`, it defaults to `"0"` and is treated as a string.

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
        "if": [
            { "expression": "format == 'csv'",     "default": "*.csv" },
            { "expression": "format == 'json'",    "default": "*.json" },
            { "expression": "format == 'parquet'", "default": "*.parquet" }
        ]
    },
    { "name": "target", "type": "dict" },
    { "name": "target.path" },
    {
        "name": "target.mode",
        "if": [
            {
                "expression": "source.format == 'parquet'",
                "validset": ["overwrite"],
                "default": "overwrite"
            },
            {
                "expression": "source.format <> 'parquet'",
                "validset": ["append", "overwrite"],
                "default": "append"
            }
        ]
    },
    { "name": "enabled", "type": "boolean", "default": True },
    { "name": "max_retries", "type": "integer", "default": 3 },
    { "name": "threshold", "type": "decimal", "default": 0.95 },
    { "name": "tags", "type": "list", "default": [] },
]

job_config = {
    "source": { "path": "/landing/prod/customers/2026-05-11", "format": "csv" },
    "target": { "path": "/bronze/prod/customers" }
}

job = control_and_setup(job_config, controls, to_object=True)
print(job.source.pattern)   # *.csv     (conditional default)
print(job.target.mode)      # append    (conditional default for non-parquet)
```

---

## Difference from `expressions`

| Feature | `expressions` | `if` |
|---|---|---|
| Changes the **value** | Yes | No |
| Changes the **control rules** (`default`, `type`, `validset`, `regex`) | No | Yes |

Use `expressions` to override a field's resolved value. Use `if` to change which rules apply to a field.
