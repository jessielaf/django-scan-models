from scan_models.validators.base_validator import BaseValidator


class VeeValidate(BaseValidator):
    def set_required(self, required: bool):
        self.validator["required"] = required
