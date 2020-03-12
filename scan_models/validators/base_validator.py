class BaseValidator:
    def __init__(self, validator: dict):
        self.validator = validator

    def set_required(self, required: bool):
        pass

    def set_min_max(self, min: float, max: float):
        pass

    def set_is_email(self):
        pass
