class AppError(Exception):
    status_code = 500
    title = "Internal Server Error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.title
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = 404
    title = "Not Found"


class ConflictError(AppError):
    status_code = 409
    title = "Conflict"


class ValidationFailedError(AppError):
    status_code = 422
    title = "Validation Error"
