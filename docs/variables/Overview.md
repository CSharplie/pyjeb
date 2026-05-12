# Variables — Overview

PyJeb supports a variable system that injects dynamic values into configuration strings at runtime. Variable placeholders are embedded directly in configuration values and resolved during the [`control_and_setup`](../api/Control-and-Setup) call.

## Variable modes

| Mode | Placeholder syntax | Source |
|---|---|---|
| `sys` | `$sys.<name>` or `$sys.<name>('format')` | Built-in system values |
| `var` | `$var.<name>` | User-supplied dictionary |
| `func` | `$func.<name>('argument')` | User-supplied callable |

---

## How placeholders work

Placeholders embedded in a configuration string are replaced by the corresponding value at runtime:

```yaml
source:
  path: "/landing/$var.env/customers/$sys.timestamp('YYYY-MM-DD')"
```

With `variables = { "env": "prod" }` and today's date `2026-05-11`, the resolved value is:

```
/landing/prod/customers/2026-05-11
```

Multiple placeholders can appear in the same value.

---

## Passing variables and functions

```python
from pyjeb import control_and_setup

variables = { "env": "prod" }

functions = {
    "get_bucket": lambda env: f"s3://my-bucket-{env}"
}

job = control_and_setup(job_config, controls, variables=variables, functions=functions)
```

---

## Pages

- [`$sys` — System variables](sys-variables): `$sys.timestamp`, `$sys.date`
- [`$var` — User variables](user-variables): `$var.<name>`
- [`$func` — Custom functions](custom-functions): `$func.<name>('argument')`
