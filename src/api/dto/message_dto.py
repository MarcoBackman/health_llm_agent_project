class HealthMessageResponseDto:
    def __init__(
            self,
            message: str,
            is_error: bool = False,
    ):
        self.message = message
        self.is_error = is_error

    def to_dict(self) -> dict:
        return {
            "response_message": self.message,
            "is_error": self.is_error,
        }

    @staticmethod
    def from_dict(data: dict) -> 'HealthMessageResponseDto':

        return HealthMessageResponseDto(**data)