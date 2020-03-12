import importlib

from scan_models.validators.base_validator import BaseValidator


class ValidatorFactory:
    @staticmethod
    def get_validator(class_name: str = "scan_models.validators.vee-validate.VeeValidate") -> BaseValidator:
        return importlib.import_module(class_name)
