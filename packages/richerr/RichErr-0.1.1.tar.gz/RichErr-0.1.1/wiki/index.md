# Welcome

## RichErr

RichErr is a tiny module that gives you basic error class, which can be used in JSON, dict, list, and other mutation

```python example.py
from richerr import RichErr

print(RichErr.convert(ValueError('Hello world!')).json(indent=2))
```

```json5
{
  "error": {
    "code": 400,
    "exception": "BadRequestException",
    "message": "Hello world!",
    "caused_by": {
      "error": {
        "code": 500,
        "exception": "ValueErrorException",
        "message": "Hello world!",
        "caused_by": null
      }
    }
  }
}
```

## Installation

### Poetry

```shell
poetry add RichErr
```

### PIP

```shell
pip install RichErr
```

## Requirements

- [x] Python 3.10+
- [x] No package dependencies

## Plugins

- [x] Supported Django Validation and ObjectNotFound errors
- [x] Supported DRF Validation errors
- [x] Supported Pydantic Validation errors

### Want to add your own error conversion?

Add direct conversion

```python
from richerr import RichErr, GatewayTimeout


class MyTimeoutError(IOError): ...


RichErr.add_conversion(MyTimeoutError, GatewayTimeout)
```

Or add conversion method

```python
from richerr import RichErr


class MyTimeoutError(IOError): ...


def _convert(err: MyTimeoutError):
    return RichErr.from_error(err, message='Something happened', code=500, name='MyTimeoutError')


RichErr.add_conversion(MyTimeoutError, _convert)
```

!!!
Subclasses will be checked before their parent, if multiple classes in same MRO will be registered.
!!!