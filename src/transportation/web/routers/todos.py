"""
Web Todos Router - Renders todo pages
"""

from fastapi import APIRouter, Request, Form, Cookie, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated, Optional

from src.transportation.api.dependencies.container import (
    get_list_todos_use_case,
    get_get_todo_use_case,
    get_create_todo_use_case,
    get_update_todo_use_case,
    get_delete_todo_use_case
)
from src.domain.use_cases.todo.list_todos import ListTodosUseCase
from src.domain.use_cases.todo.get_todo import GetTodoUseCase
from src.domain.use_cases.todo.create_todo import CreateTodoUseCase
from src.domain.use_cases.todo.update_todo import UpdateTodoUseCase
from src.domain.use_cases.todo.delete_todo import DeleteTodoUseCase
from src.data.security.jwt_service import JWTServiceImpl
from src.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    AuthenticationError,
    PermissionDeniedError
)


router = APIRouter(prefix="/todos", tags=['web-todos'])

templates = Jinja2Templates(directory="src/transportation/web/templates")


def get_current_user_from_cookie(
    access_token: Optional[str] = Cookie(None)
) -> dict:
    """Extract user from cookie token"""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"}
        )
    
    try:
        # Remove "Bearer " prefix if present
        token = access_token.replace("Bearer ", "")
        
        jwt_service = JWTServiceImpl()
        payload = jwt_service.decode_token(token)
        
        return {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'role': payload['role']
        }
    
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"}
        )


@router.get("/")
async def get_todos_page(
    request: Request,
    current_user: Annotated[dict, Depends(get_current_user_from_cookie)],
    use_case: Annotated[ListTodosUseCase, Depends(get_list_todos_use_case)]
):
    """Render todos list page"""
    try:
        todos = use_case.execute(
            user_id=current_user['user_id'],
            user_role=current_user['role']
        )
        
        return templates.TemplateResponse(
            "todos.html",
            {
                "request": request,
                "todos": [todo.to_dict() for todo in todos],
                "user": current_user
            }
        )
    
    except Exception as e:
        return templates.TemplateResponse(
            "todos.html",
            {
                "request": request,
                "todos": [],
                "user": current_user,
                "error": str(e)
            }
        )


@router.get("/add")
async def get_add_todo_page(
    request: Request,
    current_user: Annotated[dict, Depends(get_current_user_from_cookie)]
):
    """Render add todo page"""
    return templates.TemplateResponse(
        "add-todo.html",
        {
            "request": request,
            "user": current_user
        }
    )


@router.post("/add")
async def create_todo(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    priority: Annotated[int, Form()],
    current_user: Annotated[dict, Depends(get_current_user_from_cookie)],
    use_case: Annotated[CreateTodoUseCase, Depends(get_create_todo_use_case)]
):
    """Process create todo form"""
    try:
        use_case.execute(
            title=title,
            description=description,
            priority=priority,
            owner_id=current_user['user_id']
        )
        
        return RedirectResponse(url="/todos", status_code=302)
    
    except ValueError as e:
        return templates.TemplateResponse(
            "add-todo.html",
            {
                "request": request,
                "user": current_user,
                "error": str(e)
            },
            status_code=400
        )
    except Exception as e:
        return templates.TemplateResponse(
            "add-todo.html",
            {
                "request": request,
                "user": current_user,
                "error": str(e)
            },
            status_code=400
        )


@router.get("/edit/{todo_id}")
async def get_edit_todo_page(
    request: Request,
    todo_id: int,
    current_user: Annotated[dict, Depends(get_current_user_from_cookie)],
    use_case: Annotated[GetTodoUseCase, Depends(get_get_todo_use_case)]
):
    """Render edit todo page"""
    try:
        todo = use_case.execute(
            todo_id=todo_id,
            user_id=current_user['user_id'],
            user_role=current_user['role']
        )
        
        return templates.TemplateResponse(
            "edit-todo.html",
            {
                "request": request,
                "todo": todo.to_dict(),
                "user": current_user
            }
        )
    
    except EntityNotFoundError:
        return RedirectResponse(url="/todos", status_code=302)


@router.post("/edit/{todo_id}")
async def update_todo(
    request: Request,
    todo_id: int,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    priority: Annotated[int, Form()],
    current_user: Annotated[dict, Depends(get_current_user_from_cookie)],
    use_case: Annotated[UpdateTodoUseCase, Depends(get_update_todo_use_case)],
    complete: Annotated[str | None, Form()] = None  # ← Checkbox handling
):
    """Process update todo form"""
    try:
        # Convert checkbox value to boolean
        is_complete = complete == "true"
        
        use_case.execute(
            todo_id=todo_id,
            user_id=current_user['user_id'],
            user_role=current_user['role'],
            title=title,
            description=description,
            priority=priority,
            complete=is_complete
        )
        
        return RedirectResponse(url="/todos", status_code=302)
    
    except (EntityNotFoundError, PermissionDeniedError):
        return RedirectResponse(url="/todos", status_code=302)
    except ValueError as e:
        # Re-fetch todo for display
        try:
            todo = use_case.execute(todo_id, current_user['user_id'], current_user['role'])
            return templates.TemplateResponse(
                "edit-todo.html",
                {
                    "request": request,
                    "todo": todo.to_dict(),
                    "user": current_user,
                    "error": str(e)
                },
                status_code=400
            )
        except:
            return RedirectResponse(url="/todos", status_code=302)


@router.delete("/delete/{todo_id}")  # ← Changed to DELETE
async def delete_todo(
    todo_id: int,
    current_user: Annotated[dict, Depends(get_current_user_from_cookie)],
    use_case: Annotated[DeleteTodoUseCase, Depends(get_delete_todo_use_case)]
):
    """Delete todo and redirect"""
    try:
        use_case.execute(
            todo_id=todo_id,
            user_id=current_user['user_id'],
            user_role=current_user['role']
        )
    except (EntityNotFoundError, PermissionDeniedError):
        pass
    
    return RedirectResponse(url="/todos", status_code=302)