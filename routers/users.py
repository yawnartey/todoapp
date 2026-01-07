from fastapi import Depends, HTTPException, status, APIRouter 
from models import Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from pydantic import BaseModel, Field, field_validator
from passlib.context import CryptContext
from validators import validate_password_strength

router = APIRouter(
    prefix='/users', 
    tags=['users']
)

#pydantic model for the password change request
class UserVerification(BaseModel):
    current_password: str
    new_password: str = Field(min_length=4)

    @field_validator('new_password')
    def validate_new_password(cls, v):
        return validate_password_strength(v)

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

#add bycrypt context for hashing the user's password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#get a user that is currently logged in
@router.get("/", status_code=status.HTTP_200_OK)
async def read_users(user: user_dependency, db: db_dependency): 
    if user is None : 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


#allow a user that is logged in to change their current password
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification): 
    
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    #get user from database
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None: 
        raise HTTPException(status_code=404, detail='User not found.')
    
    #verify current password 
    if not bcrypt_context.verify(user_verification.current_password, user_model.hashed_password):
        raise HTTPException(status_code=400, detail='Error on password change. Verify that password is correct')
    
    #hash and update the new password 
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    
    db.add(user_model)
    db.commit()
    

#update user phone number    
@router.put("/update_phone/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number:str): 
    
    if user is None: 
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    #get user from database
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None: 
        raise HTTPException(status_code=404, detail='User not found.')

    #update the user phone number
    user_model.phone_number = phone_number
    
    db.add(user_model)
    db.commit()