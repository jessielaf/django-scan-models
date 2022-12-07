from pydoc import locate
from typing import Type


from scan_models.generator.base_generator import BaseGenerator
from scan_models.settings import get_setting


class Factory:
    @staticmethod
    def get_validator() -> Type[BaseGenerator]:
        generator = locate(get_setting("validator"))

        if not issubclass(generator, BaseGenerator):
            raise TypeError("Validator is not of type BaseGenerator")

        return generator
