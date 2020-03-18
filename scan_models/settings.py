from django.conf import settings

SETTING_NAME = "SCAN_MODELS"

DEFAULT_SETTINGS = {"mapping": {}, "validator": "scan_models.validators.VeeValidate"}


def get_setting(name: str):
    """
    Gets the setting for scan models

    Args:
        name: Name of the setting

    Returns: Value fo the setting
    """

    setting = getattr(settings, SETTING_NAME) if hasattr(settings, SETTING_NAME) else DEFAULT_SETTINGS

    if name not in setting:
        raise ValueError(f"{name} not found in {SETTING_NAME} or in default settings")

    return setting[name]
