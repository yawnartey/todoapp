"""
Todos router - Clean Architecture version (API ONLY)
Based on: TodoApp/routers/todos.py
"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Path

from src.transportation.api.schemas.todo_schema import TodoCreate, TodoUpdate, TodoResponse
from src.transportation.api.dependencies.auth import CurrentUser
from src.transportation.api.dependencies.container import (
    get_create_todo_use_case,
    get_get_todo_use_case,
    get_list_todos_use_case,
    get_update_todo_use_case,
    get_delete_todo_use_case
)
from src.domain.use_cases.todo.create_todo import CreateTodoUseCase
from src.domain.use_cases.todo.get_todo import GetTodoUseCase
from src.domain.use_cases.todo.list_todos import ListTodosUseCase
from src.domain.use_cases.todo.update_todo import UpdateTodoUseCase
from src.domain.use_cases.todo.delete_todo import DeleteTodoUseCase
from src.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    PermissionDeniedError
)


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TodoResponse])
async def read_all(
    current_user: CurrentUser,
    use_case: Annotated[ListTodosUseCase, Depends(get_list_todos_use_case)]
):
    """Get all todos for current user"""
    todos = use_case.execute(
        user_id=current_user['user_id'],
        user_role=current_user['role']
    )
    return [TodoResponse(**todo.to_dict()) for todo in todos]


@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read_by_id(
    current_user: CurrentUser,
    use_case: Annotated[GetTodoUseCase, Depends(get_get_todo_use_case)],
    todo_id: int = Path(gt=0)
):
    """Get a specific todo by ID"""
    try:
        todo = use_case.execute(
            todo_id=todo_id,
            user_id=current_user['user_id'],
            user_role=current_user['role']
        )
        return TodoResponse(**todo.to_dict())
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found.'
        )
    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to access this todo.'
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
async def create_todo(
    todo_data: TodoCreate,
    current_user: CurrentUser,
    use_case: Annotated[CreateTodoUseCase, Depends(get_create_todo_use_case)]
):
    """Create a new todo"""
    try:
        todo = use_case.execute(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            complete=False,
            owner_id=current_user['user_id']
        )
        return TodoResponse(**todo.to_dict())
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    todo_data: TodoUpdate,
    current_user: CurrentUser,
    use_case: Annotated[UpdateTodoUseCase, Depends(get_update_todo_use_case)],
    todo_id: int = Path(gt=0)
):
    """Update an existing todo"""
    try:
        use_case.execute(
            todo_id=todo_id,
            user_id=current_user['user_id'],
            user_role=current_user['role'],
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            complete=todo_data.complete
        )
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found.'
        )
    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to modify this todo.'
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(
    current_user: CurrentUser,
    use_case: Annotated[DeleteTodoUseCase, Depends(get_delete_todo_use_case)],
    todo_id: int = Path(gt=0)
):
    """Delete a todo"""
    try:
        use_case.execute(
            todo_id=todo_id,
            user_id=current_user['user_id'],
            user_role=current_user['role']
        )
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found.'
        )
    except PermissionDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to delete this todo.'
        )