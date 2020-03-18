class BaseValidator:
    def set_required(self, validator: dict, required: bool):
        pass

    def set_max_length(self, validator: dict, max_length: int):
        pass

    def set_max_value(self, validator: dict, max_value: float):
        pass

    def set_min_value(self, validator: dict, min_value: float):
        pass

    def set_is_email(self, validator: dict):
        pass
