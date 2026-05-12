# Variables — System Variables (`$sys`)

System variables are built-in dynamic values provided by PyJeb. They require no configuration and are resolved automatically at runtime.

## Available variables

| Variable | Description | Default format |
|---|---|---|
| `$sys.timestamp` | Current date and time | `YYYYMMDDHHMMSS` |
| `$sys.timestamp('format')` | Current date and time with a custom format | Custom |
| `$sys.date` | Current date | `YYYYMMDD` |
| `$sys.date('format')` | Current date with a custom format | Custom |

---

## Format tokens

| Token | Meaning | Example |
|---|---|---|
| `YYYY` | 4-digit year | `2026` |
| `MM` | 2-digit month | `05` |
| `DD` | 2-digit day | `11` |
| `hh` | 2-digit hour (24h) | `14` |
| `mm` | 2-digit minute | `30` |
| `ss` | 2-digit second | `00` |

---

## Format examples

| Placeholder | Output (2026-05-11 14:30:00) |
|---|---|
| `$sys.timestamp` | `20260511143000` |
| `$sys.timestamp('YYYY-MM-DD')` | `2026-05-11` |
| `$sys.timestamp('YYYY/MM/DD hh:mm:ss')` | `2026/05/11 14:30:00` |
| `$sys.date` | `20260511` |
| `$sys.date('YYYY-MM-DD')` | `2026-05-11` |

---

## Example

Use `$sys.timestamp` to build a dated source path:

```yaml
# job.yaml
ingest_customers:
  source:
    path: "/landing/prod/customers/$sys.timestamp('YYYY-MM-DD')"
    format: "csv"
  target:
    path: "/bronze/prod/customers"
```

```python
from pyjeb import control_and_setup

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
    "source": {
        "path": "/landing/prod/customers/$sys.timestamp('YYYY-MM-DD')",
        "format": "csv"
    },
    "target": { "path": "/bronze/prod/customers" }
}

job = control_and_setup(job_config, controls, to_object=True)
print(job.source.path)
# /landing/prod/customers/2026-05-11
```
