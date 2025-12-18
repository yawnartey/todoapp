from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth', 
    tags=['auth']
)

'''
below is required for JWT authentication. this will work together to add a signature to ensure that JWT is secured and authorised 
'''
SECRET_KEY = '986daeb59930f13caea6f25da3b66c92982ca5d4f47684cd46a61d1e3868cdd5'
ALGORITHM = 'HS256'

#using passlib/bcrypt to encrypt(hash) the user password 
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


''' 
a function to authenticate user and check wether their credentials matches what is in the database before allowing the user login access
this function is called in the router.post("/token") api method when authentication the user 
'''
def authenticate_user(username:str, password:str, db): 
    user = db.query(Users).filter(Users.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_password): 
        return False
    return user


'''
this function below generates a jwt access token for the user
'''
def create_access_token(username: str, user_id: int, role:str,  expires_delta: timedelta): 
    
    encode = {'sub': username, 'id': user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        
'''
this function allows for every api endpoint to be able to verify the current user 
'''        
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]): 
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        
        if username is None or user_id is None: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return{'username': username, 'id': user_id, 'user_role' :user_role}

    except JWTError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
'''
this class is a pydantic model for creating roles in the database
'''
class CreateUserRequest(BaseModel): 
    username: str 
    email: str 
    first_name: str 
    last_name: str 
    password: str 
    role: str
    phone_number: str
    
'''
this class is used to return proper key-value pair output for our access token
'''
class Token(BaseModel): 
    access_token: str
    token_type: str


#create the database dependency
def get_db(): 
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

#open up the database connection as a dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users (
        email = create_user_request.email, 
        username = create_user_request.username, 
        first_name = create_user_request.first_name, 
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        phone_number = create_user_request.phone_number, 
        hashed_password = bcrypt_context.hash(create_user_request.password), 
        is_active = True
    )
    
    db.add(create_user_model)
    db.commit()
     
     
'''
authenticating the provided user credentials and ensuring that they match what is in the database. since the password in the database has been hased, 
it needs to be rehashed (for lack of words for unharshed) and then the right access granted
'''
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency): 
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
    token = create_access_token (user.username, user.id, user.role, timedelta(minutes=20))
    return {
        'access_token': token, 
        'token_type': 'bearer'
    }
