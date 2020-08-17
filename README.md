# Django scan models

A validator agnostic parser for django models to frontend validation and forms

To make optimal use of this package you can use [Vue scan field](https://github.com/jessielaf/vue-scan-field). This package will **automatically** generate forms based on the generated json file.

![Coverage](./coverage.svg)

## Install
```
pip install django-scan-models
```

Add `scan_models` to your installed apps in your `settings.py`
```python
INSTALLED_APPS = [
    ...
    "scan_models"
]
```

Lastly you can add the mapping to your `settings.py`
```python
SCAN_MODELS = {
    "mapping": {
        "tests.TestModel": "../frontend/tests/validator.json"
    }
}
```

## Running

```
python manage.py scan_models
```

This will output:
```json
{
    "email": {
        "validator": {
          "required": true,
          "max": 254,
          "email": true
        },
        "attributes": {
          "type": "email"
        }
    }
}
```

**Options**

| Short | Long       | Default   | Description                              | Example |
|-------|------------|-----------|------------------------------------------|---------|
| `-m`  | `--model`  | -       | The model which should be parsed to a validator | `tests.TestModel` |

## Settings

### Mapping

The mapping of models to validator json file

```python
# Example
SCAN_MODELS = {
    ...
    "mapping": {
        "tests.TestModel": "../frontend/tests/validator.json"
    }
}
```

### Camelize

**Default**: `False`

Camelize the field name in the json. For example `email_address` will become `emailAddress`.

 ```python
# Example
SCAN_MODELS = {
    ...
    "camelize": True
}
```


### Verbosity

**Default**: `1`

Verbosity dictates how much extra data gets added to the json file. The options are

| Verbosity level | Effect |
| --------------- | ------ |
| `0`               | This option creates the smallest json file. This will remove everything that is empty. For example if the validator is empty the validator is not added to the json file | 
| `1`               | Verbosity 1 is more consistent than 0 because this option **always** adds the validator and attributes fields. |
| `2`               | You **need** to use this option when you use the [`vue-scan-field`](https://github.com/jessielaf/vue-scan-field) package. This adds `element` to `attributes` |

 ```python
# Example
SCAN_MODELS = {
    ...
    "verbosity": 0
}
```

### Validator

**Default**: `scan_models.validator.VeeValidate`

The validator which is used by the frontend. Options are:
- `scan_models.validator.VeeValidate`

```python
# Example
SCAN_MODELS = {
    ...
    "validator": "scan_models.validator.VeeValidate"
}
```

#### Custom validator

To create your custom validator just import BaseValidator and override the functions.

```python
# Example
from scan_models.validators.base_validator import BaseValidator


class CustomValidator(BaseValidator):
    def set_required(self, validator: dict, required: bool):
        validator["custom_required"] = required
```

## Testing

Running the tests can be done with:
```
coverage run --source=scan_models/ manage.py test && coverage-badge -fo coverage.svg
```

## Contributing

You can create a pull request. 

Formatting is done with black as such:
```
black . --line-length 120
```
