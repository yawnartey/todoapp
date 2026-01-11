# transportation/api/dependencies/__init__.py
from .database import get_db
from .auth import (
    get_current_user,
    get_current_user_id,
    get_current_user_role,
    require_admin
)
from .container import (
    get_todo_repository,
    get_user_repository,
    get_password_service,
    get_auth_service,
    get_create_todo_use_case,
    get_get_todo_use_case,
    get_list_todos_use_case,
    get_update_todo_use_case,
    get_delete_todo_use_case,
    get_register_user_use_case,
    get_authenticate_user_use_case,
    get_get_user_use_case,
    get_update_user_password_use_case,
    get_update_user_phone_use_case
)

__all__ = [
    # Database
    'get_db',
    # Auth
    'get_current_user',
    'get_current_user_id',
    'get_current_user_role',
    'require_admin',
    # Container - Repositories
    'get_todo_repository',
    'get_user_repository',
    # Container - Services
    'get_password_service',
    'get_auth_service',
    # Container - Todo Use Cases
    'get_create_todo_use_case',
    'get_get_todo_use_case',
    'get_list_todos_use_case',
    'get_update_todo_use_case',
    'get_delete_todo_use_case',
    # Container - User Use Cases
    'get_register_user_use_case',
    'get_authenticate_user_use_case',
    'get_get_user_use_case',
    'get_update_user_password_use_case',
    'get_update_user_phone_use_case'
]