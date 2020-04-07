from typing import Type

from scan_models.settings import get_setting
from scan_models.validators.base_validator import BaseValidator
from pydoc import locate


class Factory:
    @staticmethod
    def get_validator() -> Type[BaseValidator]:
        validator = locate(get_setting("validator"))

        if not issubclass(validator, BaseValidator):
            raise TypeError("Validator is not of type BaseValidator")

        return validator
