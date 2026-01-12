"""
Dependency Injection Container
Provides use cases with their dependencies wired up
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

# Database dependency
from src.transportation.api.dependencies.database import get_db

# Repository implementations
from src.data.database.repositories.todo_repository_impl import TodoRepositoryImpl
from src.data.database.repositories.user_repository_impl import UserRepositoryImpl

# Service implementations
from src.data.security.password_service import PasswordServiceImpl
from src.data.security.jwt_service import JWTServiceImpl

# Todo use cases
from src.domain.use_cases.todo.create_todo import CreateTodoUseCase
from src.domain.use_cases.todo.get_todo import GetTodoUseCase
from src.domain.use_cases.todo.list_todos import ListTodosUseCase
from src.domain.use_cases.todo.update_todo import UpdateTodoUseCase
from src.domain.use_cases.todo.delete_todo import DeleteTodoUseCase

# User use cases
from src.domain.use_cases.user.register_user import RegisterUserUseCase
from src.domain.use_cases.user.authenticate_user import AuthenticateUserUseCase
from src.domain.use_cases.user.get_user import GetUserUseCase
from src.domain.use_cases.user.update_user_password import UpdateUserPasswordUseCase
from src.domain.use_cases.user.update_user_phone import UpdateUserPhoneUseCase
from src.domain.use_cases.user.delete_user import DeleteUserUseCase


# Repository Dependencies
def get_todo_repository(
    db: Annotated[Session, Depends(get_db)]
) -> TodoRepositoryImpl:
    return TodoRepositoryImpl(db)


def get_user_repository(
    db: Annotated[Session, Depends(get_db)]
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)

# Service Dependencies
def get_password_service() -> PasswordServiceImpl:
    return PasswordServiceImpl()

def get_auth_service() -> JWTServiceImpl:
    return JWTServiceImpl()

# Todo Use Case Dependencies
def get_create_todo_use_case(
    todo_repository: Annotated[TodoRepositoryImpl, Depends(get_todo_repository)]
) -> CreateTodoUseCase:
    return CreateTodoUseCase(todo_repository)

def get_get_todo_use_case(
    todo_repository: Annotated[TodoRepositoryImpl, Depends(get_todo_repository)]
) -> GetTodoUseCase:
    return GetTodoUseCase(todo_repository)

def get_list_todos_use_case(
    todo_repository: Annotated[TodoRepositoryImpl, Depends(get_todo_repository)]
) -> ListTodosUseCase:
    return ListTodosUseCase(todo_repository)


def get_update_todo_use_case(
    todo_repository: Annotated[TodoRepositoryImpl, Depends(get_todo_repository)]
) -> UpdateTodoUseCase:
    return UpdateTodoUseCase(todo_repository)


def get_delete_todo_use_case(
    todo_repository: Annotated[TodoRepositoryImpl, Depends(get_todo_repository)]
) -> DeleteTodoUseCase:
    return DeleteTodoUseCase(todo_repository)

# User Use Case Dependencies
def get_register_user_use_case(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    password_service: Annotated[PasswordServiceImpl, Depends(get_password_service)]
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository, password_service)


def get_authenticate_user_use_case(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    password_service: Annotated[PasswordServiceImpl, Depends(get_password_service)],
    auth_service: Annotated[JWTServiceImpl, Depends(get_auth_service)]
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(user_repository, password_service, auth_service)


def get_get_user_use_case(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> GetUserUseCase:
    return GetUserUseCase(user_repository)


def get_update_user_password_use_case(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
    password_service: Annotated[PasswordServiceImpl, Depends(get_password_service)]
) -> UpdateUserPasswordUseCase:
    return UpdateUserPasswordUseCase(user_repository, password_service)


def get_update_user_phone_use_case(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> UpdateUserPhoneUseCase:
    return UpdateUserPhoneUseCase(user_repository)


def get_delete_user_use_case(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repository)