# domain/exceptions/domain_exceptions.py

class DomainException(Exception):
    """Base exception for all domain-related errors"""
    pass


class ValidationError(DomainException):
    """Raised when entity validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found"""
    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id
        self.message = f"{entity_name} with id {entity_id} not found"
        super().__init__(self.message)


class PermissionDeniedError(DomainException):
    """Raised when user doesn't have permission to perform action"""
    def __init__(self, message: str = "Permission denied"):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(DomainException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(AuthenticationError):
    """Raised when user credentials are invalid"""
    def __init__(self, message: str = "Invalid username or password"):
        self.message = message
        super().__init__(self.message)


class PasswordStrengthError(ValidationError):
    """Raised when password doesn't meet strength requirements"""
    def __init__(self, message: str):
        super().__init__(message)


class DuplicateEntityError(DomainException):
    """Raised when trying to create duplicate entity"""
    def __init__(self, entity_name: str, field: str, value: str):
        self.entity_name = entity_name
        self.field = field
        self.value = value
        self.message = f"{entity_name} with {field} '{value}' already exists"
        super().__init__(self.message)


class InactiveUserError(AuthenticationError):
    """Raised when trying to authenticate inactive user"""
    def __init__(self, message: str = "User account is inactive"):
        self.message = message
        super().__init__(self.message)