from fastapi import Depends, HTTPException, status, Path, APIRouter 
from models import Todos, Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/admin', 
    tags=['admin']
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

#get all todos
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency): 
    if user is None or user.get('user_role') != 'admin': 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

#get all users
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency): 
    if user is None or user.get('user_role') != 'admin': 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).all()
        
@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin': 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None: 
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    
    db.commit()