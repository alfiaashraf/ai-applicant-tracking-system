class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class InvalidFileError(AppError):
    """Raised when an uploaded file fails validation."""


class PDFParseError(AppError):
    """Raised when PDF text extraction fails."""


class EmptyDocumentError(AppError):
    """Raised when a document contains no extractable text."""


class JobNotFoundError(AppError):
    """Raised when a job ID does not exist."""
