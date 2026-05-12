# Exceptions

PyJeb raises typed exceptions when a configuration or control definition is invalid.

All exceptions can be imported from `pyjeb.exception`:

```python
from pyjeb.exception import (
    NotProvidedParameterException,
    EmptyParameterException,
    InvalidTypeParameterException,
    InvalidValueParameterException,
    InvalidControlException,
    CustomFunctionException,
)
```

## Exception hierarchy

```
Exception
├── InvalidParameterException
│   ├── NotProvidedParameterException
│   ├── EmptyParameterException
│   ├── InvalidTypeParameterException
│   └── InvalidValueParameterException
├── InvalidControlException
└── CustomFunctionException
```

---

## `NotProvidedParameterException`

**Raised when**: a required field (no `default`) is absent from the configuration.

```python
controls = [
    { "name": "source", "type": "dict" },
    { "name": "source.path" },           # required — no default
    { "name": "source.format", "validset": ["csv", "json", "parquet"] },
    # ...
]

job_config = {
    "source": { "format": "csv" },       # source.path is missing
    "target": { "path": "/bronze/prod/customers" }
}
```

```python
from pyjeb.exception import NotProvidedParameterException

try:
    job = control_and_setup(job_config, controls)
except NotProvidedParameterException as e:
    print(e)
# The property 'source.path' is not setup and have no default value
```

---

## `EmptyParameterException`

**Raised when**: a required field is present but its value is empty (`""` or `None`).

```python
job_config = {
    "source": { "path": "", "format": "csv" },   # path is empty
    "target": { "path": "/bronze/prod/customers" }
}
```

```python
from pyjeb.exception import EmptyParameterException

try:
    job = control_and_setup(job_config, controls)
except EmptyParameterException as e:
    print(e)
# Property 'source.path' can't be empty
```

---

## `InvalidTypeParameterException`

**Raised when**: a field value does not match the declared type.

```python
job_config = {
    "source": { "path": "/landing/prod/customers", "format": "csv" },
    "target": { "path": "/bronze/prod/customers" },
    "max_retries": "not-a-number"    # declared as integer
}
```

```python
from pyjeb.exception import InvalidTypeParameterException

try:
    job = control_and_setup(job_config, controls)
except InvalidTypeParameterException as e:
    print(e)
# Property 'max_retries' has invalid value 'not-a-number' (type must be integer)
```

---

## `InvalidValueParameterException`

**Raised when**: a field value is not in the allowed `validset`, or does not match the `regex` pattern.

```python
job_config = {
    "source": { "path": "/landing/prod/customers", "format": "xml" },  # not in validset
    "target": { "path": "/bronze/prod/customers" }
}
```

```python
from pyjeb.exception import InvalidValueParameterException

try:
    job = control_and_setup(job_config, controls)
except InvalidValueParameterException as e:
    print(e)
# Property 'source.format' ('csv', 'json', 'parquet') has invalid value 'xml'
```

---

## `InvalidControlException`

**Raised when**: a control definition is malformed. This includes invalid expression syntax or a field path referenced in an expression that cannot be resolved.

```python
controls_bad = [
    { "name": "source", "type": "dict" },
    { "name": "source.path" },
    {
        "name": "source.pattern",
        "default": "*",
        "expressions": ["if format EQUALS 'csv' return '*.csv'"]  # invalid syntax
    },
]
```

```python
from pyjeb.exception import InvalidControlException

try:
    job = control_and_setup(job_config, controls_bad)
except InvalidControlException as e:
    print(e)
```

---

## `CustomFunctionException`

**Raised when**: a custom function registered in `functions` raises an exception during execution.

```python
functions = {
    "get_bucket": lambda env: int(env)   # will fail if env is not a number
}

job_config = {
    "source": { "path": "$func.get_bucket('prod')", "format": "csv" },
    "target": { "path": "/bronze/prod/customers" }
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

## Catching all PyJeb exceptions

```python
from pyjeb.exception import InvalidParameterException, InvalidControlException, CustomFunctionException

try:
    job = control_and_setup(job_config, controls, variables=variables)
except InvalidParameterException as e:
    print(f"Configuration error: {e}")
except InvalidControlException as e:
    print(f"Control definition error: {e}")
except CustomFunctionException as e:
    print(f"Custom function error: {e}")
```
