from scan_models.validators.base_validator import BaseValidator


class VeeValidate(BaseValidator):
    def set_required(self, validator: dict):
        validator["required"] = True

    def set_max_length(self, validator: dict, max_length: int):
        validator["max"] = max_length

    def set_choices(self, validator: dict, choices: list):
        validator["oneOf"] = choices

    def set_max_value(self, validator: dict, max_value: float):
        validator["max_value"] = max_value

    def set_min_value(self, validator: dict, min_value: float):
        validator["min_value"] = min_value

    def set_is_email(self, validator: dict):
        validator["email"] = True

    def set_regex(self, validator: dict, regex: str):
        validator["regex"] = regex
