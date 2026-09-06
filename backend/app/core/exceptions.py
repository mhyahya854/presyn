"""Structured Exception Definitions for Presyn Platform."""

from typing import Any, Optional
from fastapi import HTTPException


class PresynException(Exception):
    """Base exception class for Presyn domain errors."""

    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR", details: Optional[Any] = None) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class DatabaseUnavailableException(PresynException):
    """Raised when primary database connectivity fails."""

    def __init__(self, message: str = "Database connection unavailable") -> None:
        super().__init__(message=message, error_code="DATABASE_UNAVAILABLE")


class ResourceNotFoundException(PresynException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource_type: str, identifier: Any) -> None:
        super().__init__(
            message=f"{resource_type} with identifier {identifier} not found",
            error_code="NOT_FOUND",
            details={"resource_type": resource_type, "identifier": str(identifier)},
        )


class ValidationException(PresynException):
    """Raised when input validation fails."""

    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        super().__init__(message=message, error_code="VALIDATION_ERROR", details=details)


def create_http_error(status_code: int, error_code: str, message: str) -> HTTPException:
    """Helper to generate standardized HTTP exceptions with structured details."""
    return HTTPException(
        status_code=status_code,
        detail={"error_code": error_code, "message": message},
    )
