# Getting Started

This guide walks through a complete PyJeb setup using a data ingestion job configuration as a running example.

## The scenario

You manage a set of data ingestion jobs. Each job reads files from a source path and writes them to a target path, with operational parameters (format, retries, threshold, etc.). You want to:

- Validate that required fields are present
- Apply sensible defaults for optional fields
- Inject the current date and environment name dynamically

## Step 1 — Install PyJeb

```shell
pip install pyjeb
```

## Step 2 — Write the configuration file

Create `job.yaml` with one or more job entries:

```yaml
# job.yaml
ingest_customers:
  source:
    path: "/landing/$var.env/customers/$sys.timestamp('YYYY-MM-DD')"
    format: "csv"
    pattern: "*.csv"
  target:
    path: "/bronze/$var.env/customers"
    mode: "append"
  enabled: true
  max_retries: 3
  threshold: 0.95
  tags:
    - "crm"
    - "daily"

ingest_orders:
  source:
    path: "/landing/$var.env/orders/$sys.timestamp('YYYY-MM-DD')"
    format: "json"
  target:
    path: "/bronze/$var.env/orders"
  enabled: true
```

> `$var.env` and `$sys.timestamp(...)` are PyJeb variables resolved at runtime. See [Variables](variables/overview).

## Step 3 — Define the control list

The control list describes the expected structure of each job entry:

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

See [Controls — Overview](controls/overview) for all available control fields.

## Step 4 — Apply control_and_setup

```python
import yaml
from pyjeb import control_and_setup

with open("job.yaml") as f:
    config = yaml.safe_load(f)

variables = { "env": "prod" }

for job_name, job_config in config.items():
    job = control_and_setup(job_config, controls, variables=variables, to_object=True)
    print(f"[{job_name}]")
    print(f"  source.path    = {job.source.path}")
    print(f"  source.format  = {job.source.format}")
    print(f"  source.pattern = {job.source.pattern}")
    print(f"  target.path    = {job.target.path}")
    print(f"  target.mode    = {job.target.mode}")
    print(f"  enabled        = {job.enabled}")
    print(f"  max_retries    = {job.max_retries}")
    print(f"  threshold      = {job.threshold}")
    print(f"  tags           = {job.tags}")
```

**Output** (run on 2026-05-11 with `env = "prod"`):

```
[ingest_customers]
  source.path    = /landing/prod/customers/2026-05-11
  source.format  = csv
  source.pattern = *.csv
  target.path    = /bronze/prod/customers
  target.mode    = append
  enabled        = True
  max_retries    = 3
  threshold      = 0.95
  tags           = ['crm', 'daily']

[ingest_orders]
  source.path    = /landing/prod/orders/2026-05-11
  source.format  = json
  source.pattern = *
  target.path    = /bronze/prod/orders
  target.mode    = append
  enabled        = True
  max_retries    = 3
  threshold      = 0.95
  tags           = []
```

Notice that for `ingest_orders`:
- `source.pattern` defaulted to `"*"` — not provided in the file
- `target.mode` defaulted to `"append"` — not provided in the file
- `enabled`, `max_retries`, `threshold`, `tags` all received their default values
- `$var.env` was replaced by `"prod"`
- `$sys.timestamp('YYYY-MM-DD')` was replaced by the current date

## Next steps

- Customize your control definitions: [Controls — Overview](controls/overview)
- Use variables and functions: [Variables — Overview](variables/overview)
- Handle validation errors: [Exceptions](exceptions)
