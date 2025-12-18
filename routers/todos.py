from fastapi import Depends, HTTPException, status, Path, APIRouter, Request
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user

from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/todos', 
    tags=['todos']
)

#create the database dependency
def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

#open up the database connection as a dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

#depends on the user authentication created in the auth.py file
user_dependency = Annotated[dict, Depends(get_current_user)]

#import frontend templates 
templates = Jinja2Templates(directory="templates")

class TodoRequest(BaseModel): 
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=500)
    priority: int = Field(gt=0, lt=11)
    complete: bool


def redirect_to_login(): 
    redirect_response = RedirectResponse(url = "/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


'''
pages that are being rendered to/from the frontend 
start from below
'''
@router.get("/todo-page")
async def render_todo_page(request: Request, db:db_dependency): 
    try: 
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None: 
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        
        return templates.TemplateResponse("todos.html", {"request": request, "todos": todos, "user": user})

    except Exception as e:
        print(f"Error: {e}")
        return redirect_to_login()
    
    
@router.get("/add-todo-page")
async def render_todo_page(request: Request, db:db_dependency): 
    try: 
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None: 
            return redirect_to_login()

        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

    except Exception as e:
        print(f"Error: {e}")
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db:db_dependency): 
    try: 
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None: 
            return redirect_to_login()
        
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo,  "user": user})

    except Exception as e:
        print(f"Error: {e}")
        return redirect_to_login()

'''
api endpoints also start from 
the below
'''
#get todo, but this time based on an authenticated user
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):  
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

    
#get todo based on todo id and also this time only authenticated users can be able to get the todo item based on the id
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK) 
async def read_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)): 
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None: 
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


#create post request method to send records to the database
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request:TodoRequest): 
    #ensure the user that is making the post request is authenticated
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    
    db.add(todo_model)
    db.commit()
    
#create a put request method to update records in the database
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request:TodoRequest, todo_id: int = Path(gt=0)): 
    
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    #ensure the user that is making the postdb: db_dependency, todo_request: TodoRequest, todo_id:int = Path(gt=0)): 
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None: 
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
#create a delete request method to remove an item from the todo list
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None: 
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    
    db.commit()