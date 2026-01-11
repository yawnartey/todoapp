# domain/interfaces/repositories/__init__.py
from .todo_repository import ITodoRepository
from .user_repository import IUserRepository

__all__ = ['ITodoRepository', 'IUserRepository']