class AppError(Exception):
    status_code = 500
    error_type = "internal-error"
    title = "Internal Server Error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.title
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = 404
    error_type = "not-found"
    title = "Not Found"


class ConflictError(AppError):
    status_code = 409
    error_type = "conflict"
    title = "Conflict"


class ValidationFailedError(AppError):
    status_code = 422
    error_type = "validation-error"
    title = "Validation Error"
