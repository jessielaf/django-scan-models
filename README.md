# Django scan models
Parse django models to frontend validation

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

Running the scan models can be done with this command:
```
python manage.py scan_models
```
