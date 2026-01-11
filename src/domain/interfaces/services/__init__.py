# domain/interfaces/services/__init__.py
from .auth_service import IAuthService
from .password_service import IPasswordService

__all__ = ['IAuthService', 'IPasswordService']