"""
API Layer - Routers, schemas, and dependencies
"""

from .routers import auth_router, todos_router, users_router, admin_router
from .schemas import (
    TodoCreate, TodoUpdate, TodoResponse,
    UserCreate, UserResponse, UserPasswordUpdate, UserPhoneUpdate,
    Token, TokenData
)

__all__ = [
    # Routers
    'auth_router',
    'todos_router',
    'users_router',
    'admin_router',
    # Schemas
    'TodoCreate',
    'TodoUpdate',
    'TodoResponse',
    'UserCreate',
    'UserResponse',
    'UserPasswordUpdate',
    'UserPhoneUpdate',
    'Token',
    'TokenData',
]