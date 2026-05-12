# Variables — User Variables (`$var`)

User variables let you inject custom named values into configuration strings at runtime. They are passed as a dictionary to [`control_and_setup`](../api/Control-and-Setup) via the `variables` parameter.

## Syntax

```
$var.<name>
```

The placeholder is replaced by the value in the `variables` dictionary whose key matches `<name>`.

---

## Passing variables

```python
variables = { "env": "prod" }

job = control_and_setup(job_config, controls, variables=variables)
```

---

## Example

```yaml
# job.yaml
ingest_customers:
  source:
    path: "/landing/$var.env/customers/$sys.timestamp('YYYY-MM-DD')"
    format: "csv"
  target:
    path: "/bronze/$var.env/customers"
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

variables = { "env": "prod" }

job_config = {
    "source": {
        "path": "/landing/$var.env/customers/$sys.timestamp('YYYY-MM-DD')",
        "format": "csv"
    },
    "target": { "path": "/bronze/$var.env/customers" }
}

job = control_and_setup(job_config, controls, variables=variables, to_object=True)
print(job.source.path)    # /landing/prod/customers/2026-05-11
print(job.target.path)    # /bronze/prod/customers
```

---

## Multiple variables

```python
variables = {
    "env": "prod",
    "region": "eu-west-1"
}
```

```yaml
source:
  path: "/landing/$var.env/$var.region/customers/$sys.timestamp('YYYY-MM-DD')"
```

Resolves to:

```
/landing/prod/eu-west-1/customers/2026-05-11
```

---

## Unresolved variables

If a variable name is not found in the `variables` dictionary, the placeholder is left as-is in the string. No error is raised.

```python
variables = {}  # env not defined
# result: "/landing/$var.env/customers/2026-05-11"  — $var.env is not replaced
```

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
    job = control_and_setup(job_config, controls, variables=variables, to_object=True)
    print(f"{job_name}: {job.source.path} → {job.target.path}")
```
