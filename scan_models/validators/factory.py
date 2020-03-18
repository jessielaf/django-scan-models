from typing import Type

from scan_models.settings import get_setting
from scan_models.validators.base_validator import BaseValidator
from pydoc import locate

# todo: Add validator list to readme
class ValidatorFactory:
    @staticmethod
    def get_validator() -> Type[BaseValidator]:
        return locate(get_setting("validator"))
