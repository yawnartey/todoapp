from fastapi import Depends, HTTPException, status, Path, APIRouter 
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user

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


class TodoRequest(BaseModel): 
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=500)
    priority: int = Field(gt=0, lt=11)
    complete: bool


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