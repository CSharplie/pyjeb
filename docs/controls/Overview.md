# Controls — Overview

A **control** is a Python dictionary that describes one field of a configuration. The `controls` parameter of [`control_and_setup`](../api/Control-and-Setup) is a list of such dictionaries.

## Control fields

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | Yes | — | Dot-separated path to the field |
| `type` | string | No | `"string"` | Expected type of the value |
| `default` | any | No | — | Value to use when the field is absent |
| `validset` | list | No | — | List of allowed values or regex patterns |
| `regex` | string | No | — | Regex pattern the value must match |
| `expressions` | list | No | `[]` | List of conditional value overrides |
| `if` | list | No | `[]` | List of conditional control overrides |
| `nocheck` | boolean | No | `False` | Skip validation for this field |

---

## `name`

The dot-separated path to the target field. Nested fields use `parent.child` notation.

```python
{ "name": "source" }           # top-level field
{ "name": "source.path" }      # nested field
{ "name": "source.format" }    # sibling of source.path
```

Parent fields must be declared before their children, and must have type `"dict"` or `"list"`.

---

## `type`

The expected type for the field value. Defaults to `"string"` when omitted.

Supported values: `"string"`, `"integer"`, `"decimal"`, `"boolean"`, `"list"`, `"dict"`

```python
{ "name": "source", "type": "dict" }
{ "name": "enabled", "type": "boolean", "default": True }
{ "name": "max_retries", "type": "integer", "default": 3 }
{ "name": "threshold", "type": "decimal", "default": 0.95 }
{ "name": "tags", "type": "list", "default": [] }
```

See [Controls — Types](types) for casting rules and details.

---

## `default`

The value to use when the field is absent from the configuration.

```python
{ "name": "source.pattern", "default": "*" }
{ "name": "target.mode", "default": "append" }
{ "name": "max_retries", "type": "integer", "default": 3 }
{ "name": "tags", "type": "list", "default": [] }
```

If `default` is not set, the field is **required** — a `NotProvidedParameterException` is raised when it is missing.

---

## `validset`

A list of allowed values. The field value must match one entry exactly, or match one entry as a regex pattern.

```python
{ "name": "source.format", "validset": ["csv", "json", "parquet"] }
{ "name": "target.mode", "default": "append", "validset": ["append", "overwrite"] }
```

See [Controls — Validset](validset).

---

## `regex`

A regex pattern the field value must match.

```python
{ "name": "source.path", "regex": r"^/[a-zA-Z0-9/_\$\.\-]+$" }
```

See [Controls — Regex](regex).

---

## `expressions`

A list of conditional value expressions that can override the field value based on sibling field values.

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

See [Controls — Expressions](expressions).

---

## `if`

Conditional overrides that change the `default`, `type`, `validset`, or `regex` of a control based on sibling values.

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

See [Controls — Conditional Controls](conditional-controls).

---

## `nocheck`

When set to `True`, validation is entirely skipped for this field. The value is passed through as-is.

```python
{ "name": "metadata", "nocheck": True }
```

---

## Complete example

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
