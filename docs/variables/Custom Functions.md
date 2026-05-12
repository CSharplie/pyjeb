# Variables — Custom Functions (`$func`)

Custom functions let you inject computed values into configuration strings at runtime. They are passed as a dictionary of callables to [`control_and_setup`](../api/Control-and-Setup) via the `functions` parameter.

## Syntax

```
$func.<name>('argument')
```

The placeholder is replaced by the return value of the function named `<name>`, called with `'argument'` as its sole parameter (always passed as a string).

---

## Passing functions

```python
functions = {
    "get_bucket": lambda env: f"s3://my-bucket-{env}"
}

job = control_and_setup(job_config, controls, functions=functions)
```

---

## Example

```yaml
# job.yaml
ingest_customers:
  source:
    path: "/landing/prod/customers/$sys.timestamp('YYYY-MM-DD')"
    format: "csv"
  target:
    path: "$func.get_bucket('prod')/bronze/customers"
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

functions = {
    "get_bucket": lambda env: f"s3://my-bucket-{env}"
}

job_config = {
    "source": {
        "path": "/landing/prod/customers/$sys.timestamp('YYYY-MM-DD')",
        "format": "csv"
    },
    "target": { "path": "$func.get_bucket('prod')/bronze/customers" }
}

job = control_and_setup(job_config, controls, functions=functions, to_object=True)
print(job.target.path)
# s3://my-bucket-prod/bronze/customers
```

---

## Error handling

If a custom function raises an exception, PyJeb wraps it in a `CustomFunctionException`.

```python
functions = {
    "get_bucket": lambda env: int(env)   # will fail if env is not a number
}
```

```python
from pyjeb.exception import CustomFunctionException

try:
    job = control_and_setup(job_config, controls, functions=functions)
except CustomFunctionException as e:
    print(e)
# Function 'func.get_bucket' raise an error with parameter 'prod'
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

functions = {
    "get_bucket": lambda env: f"s3://my-bucket-{env}"
}

for job_name, job_config in config.items():
    job = control_and_setup(
        job_config,
        controls,
        variables=variables,
        functions=functions,
        to_object=True
    )
    print(f"{job_name}: {job.target.path}")
```
