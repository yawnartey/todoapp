# domain/exceptions/__init__.py
from .domain_exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    PermissionDeniedError,
    AuthenticationError,
    InvalidCredentialsError,
    PasswordStrengthError,
    DuplicateEntityError,
    InactiveUserError
)

__all__ = [
    'DomainException',
    'ValidationError',
    'EntityNotFoundError',
    'PermissionDeniedError',
    'AuthenticationError',
    'InvalidCredentialsError',
    'PasswordStrengthError',
    'DuplicateEntityError',
    'InactiveUserError'
]