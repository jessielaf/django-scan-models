from scan_models.validators.base_validator import BaseValidator


class VeeValidate(BaseValidator):
    def set_required(self, validator: dict, required: bool):
        validator["required"] = required

    def set_max_length(self, validator: dict, max_length: int):
        validator["max"] = max_length

    def set_max_value(self, validator: dict, max_value: float):
        validator["max_value"] = max_value

    def set_min_value(self, validator: dict, min_value: float):
        validator["min_value"] = min_value

    def set_is_email(self, validator: dict):
        validator["email"] = True
