# domain/use_cases/__init__.py
from .todo import (
    CreateTodoUseCase,
    GetTodoUseCase,
    ListTodosUseCase,
    UpdateTodoUseCase,
    DeleteTodoUseCase
)
from .user import (
    RegisterUserUseCase,
    AuthenticateUserUseCase,
    GetUserUseCase,
    UpdateUserPasswordUseCase,
    UpdateUserPhoneUseCase
)

__all__ = [
    # Todo use cases
    'CreateTodoUseCase',
    'GetTodoUseCase',
    'ListTodosUseCase',
    'UpdateTodoUseCase',
    'DeleteTodoUseCase',
    # User use cases
    'RegisterUserUseCase',
    'AuthenticateUserUseCase',
    'GetUserUseCase',
    'UpdateUserPasswordUseCase',
    'UpdateUserPhoneUseCase'
]