"""
Domain interfaces - Abstract contracts for repositories and services
"""

from .repositories import ITodoRepository, IUserRepository
from .services import IAuthService, IPasswordService

__all__ = [
    'ITodoRepository',
    'IUserRepository',
    'IAuthService',
    'IPasswordService',
]