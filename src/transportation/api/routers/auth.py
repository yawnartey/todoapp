"""
Authentication router - Clean Architecture version (API ONLY)
Based on: TodoApp/routers/auth.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.transportation.api.schemas.user_schema import UserCreate, UserResponse
from src.transportation.api.schemas.auth_schema import Token
from src.transportation.api.dependencies.container import (
    get_register_user_use_case,
    get_authenticate_user_use_case
)
from src.domain.use_cases.user.register_user import RegisterUserUseCase
from src.domain.use_cases.user.authenticate_user import AuthenticateUserUseCase
from src.domain.exceptions.domain_exceptions import (
    DuplicateEntityError,
    InvalidCredentialsError,
    PasswordStrengthError,
    InactiveUserError
)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)]
):
    """Register a new user"""
    try:
        user = use_case.execute(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=user_data.password,
            role=user_data.role,
            phone_number=user_data.phone_number
        )
        return UserResponse(**user.to_dict())
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except PasswordStrengthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: Annotated[AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)]
):
    """Authenticate user and return JWT token"""
    try:
        result = use_case.execute(
            username=form_data.username,
            password=form_data.password,
            token_expires_minutes=20
        )
        return Token(
            access_token=result['access_token'],
            token_type=result['token_type']
        )
    
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except InactiveUserError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User account is inactive',
            headers={'WWW-Authenticate': 'Bearer'}
        )