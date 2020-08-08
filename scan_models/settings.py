from django.conf import settings

SETTING_NAME = "SCAN_MODELS"

DEFAULT_SETTINGS = {"mapping": {}, "validator": "scan_models.validators.VeeValidate", "camelize": False, "verbosity": 2}


def get_setting(name: str):
    """
    Gets the setting for scan models

    Args:
        name: Name of the setting

    Returns: Value fo the setting
    """

    setting = getattr(settings, SETTING_NAME) if hasattr(settings, SETTING_NAME) else {}

    return setting[name] if name in setting else DEFAULT_SETTINGS[name]
