# transportation/api/routers/admin.py
"""
Admin router - Clean Architecture version
Based on: TodoApp/routers/admin.py
"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Path

from src.transportation.api.schemas.todo_schema import TodoResponse
from src.transportation.api.schemas.user_schema import UserResponse
from src.transportation.api.dependencies.auth import require_admin, AdminUser
from src.transportation.api.dependencies.container import (
    get_list_todos_use_case,
    get_delete_todo_use_case,
    get_user_repository, 
    get_delete_user_use_case
)
from src.domain.use_cases.todo.list_todos import ListTodosUseCase
from src.domain.use_cases.todo.delete_todo import DeleteTodoUseCase
from src.domain.use_cases.user.delete_user import DeleteUserUseCase
from src.data.database.repositories.user_repository_impl import UserRepositoryImpl
from src.domain.exceptions.domain_exceptions import EntityNotFoundError, PermissionDeniedError


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@router.get("/todo", status_code=status.HTTP_200_OK, response_model=List[TodoResponse])
async def read_all_todos(
    admin_user: AdminUser,
    use_case: Annotated[ListTodosUseCase, Depends(get_list_todos_use_case)]
):
    """
    Get all todos
    """
    todos = use_case.execute(
        user_id=admin_user['user_id'],
        user_role=admin_user['role']  # 'admin' - will return all todos
    )
    return [TodoResponse(**todo.to_dict()) for todo in todos]


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def read_all_users(
    admin_user: AdminUser,
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
):
    """
    Get all users
    """
    users = user_repository.get_all()
    return [UserResponse(**user.to_dict()) for user in users]


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(
    admin_user: AdminUser,
    use_case: Annotated[DeleteTodoUseCase, Depends(get_delete_todo_use_case)],
    todo_id: int = Path(gt=0)
):
    """
    Delete any todo by ID
    """
    try:
        use_case.execute(
            todo_id=todo_id,
            user_id=admin_user['user_id'],
            user_role=admin_user['role']  # 'admin' - can delete any todo
        )
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found.'
        )
        
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    admin_user: AdminUser,
    use_case: Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)],
    user_id: int = Path(gt=0)
):
    """Delete user by ID """
    try:
        use_case.execute(
            user_id=user_id,
            admin_id=admin_user['user_id'],
            admin_role=admin_user['role']
        )
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )