# Controls — Types

PyJeb supports six types for control definitions. The `type` field specifies the expected type of the configuration value. When `type` is omitted, it defaults to `"string"`.

Supported types: `string`, `integer`, `decimal`, `boolean`, `list`, `dict`

---

## `string`

Any scalar value that is not a `dict` or `list`. Numbers and booleans read from YAML or JSON are accepted as-is.

```python
{ "name": "source.path" }
{ "name": "source.format", "type": "string", "validset": ["csv", "json", "parquet"] }
{ "name": "target.mode", "type": "string", "default": "append" }
```

---

## `integer`

An integer value. Strings like `"3"` or `"-10"` with optional surrounding spaces are accepted and cast to `int`.

```python
{ "name": "max_retries", "type": "integer", "default": 3 }
```

| Input | Valid | Output |
|---|---|---|
| `3` | Yes | `3` |
| `"3"` | Yes | `3` |
| `"-10"` | Yes | `-10` |
| `"- 10"` | Yes | `-10` |
| `3.5` | No | — |
| `"abc"` | No | — |

---

## `decimal`

A floating-point value. Strings with `.` or `,` as decimal separator are accepted and cast to `float`.

```python
{ "name": "threshold", "type": "decimal", "default": 0.95 }
```

| Input | Valid | Output |
|---|---|---|
| `0.95` | Yes | `0.95` |
| `"0.95"` | Yes | `0.95` |
| `"0,95"` | Yes | `0.95` |
| `"-1.5"` | Yes | `-1.5` |
| `"abc"` | No | — |

---

## `boolean`

A boolean value. Strings `"true"` and `"false"` (case-insensitive) are accepted and cast to `bool`.

```python
{ "name": "enabled", "type": "boolean", "default": True }
```

| Input | Valid | Output |
|---|---|---|
| `True` | Yes | `True` |
| `False` | Yes | `False` |
| `"true"` | Yes | `True` |
| `"False"` | Yes | `False` |
| `1` | No | — |

---

## `list`

A list value. A scalar value (string, number) is automatically wrapped in a single-element list.

```python
{ "name": "tags", "type": "list", "default": [] }
```

| Input | Valid | Output |
|---|---|---|
| `["crm", "daily"]` | Yes | `["crm", "daily"]` |
| `"crm"` | Yes | `["crm"]` |
| `3` | Yes | `[3]` |
| `{"key": "val"}` | Yes | `[{"key": "val"}]` |

---

## `dict`

A nested dictionary. Used to declare parent fields that contain child controls. Child fields are declared as separate controls using dot notation.

```python
{ "name": "source", "type": "dict" },
{ "name": "source.path" },
{ "name": "source.format", "validset": ["csv", "json", "parquet"] },
{ "name": "source.pattern", "default": "*" },
```

No casting is applied for `dict` fields; the value must already be a Python `dict`.

---

## Type summary for the running example

Given this configuration:

```yaml
ingest_customers:
  source:
    path: "/landing/prod/customers/2026-05-11"
    format: "csv"
    pattern: "*.csv"
  target:
    path: "/bronze/prod/customers"
    mode: "append"
  enabled: true
  max_retries: 3
  threshold: 0.95
  tags:
    - "crm"
    - "daily"
```

And these controls:

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

After `control_and_setup`, the Python types are:

| Field | Python type |
|---|---|
| `source` | `dict` |
| `source.path` | `str` |
| `source.format` | `str` |
| `source.pattern` | `str` |
| `target` | `dict` |
| `target.path` | `str` |
| `target.mode` | `str` |
| `enabled` | `bool` |
| `max_retries` | `int` |
| `threshold` | `float` |
| `tags` | `list` |
