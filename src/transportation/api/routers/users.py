"""
Users router - Clean Architecture version
Based on: TodoApp/routers/users.py
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from src.transportation.api.schemas.user_schema import (
    UserResponse,
    UserPasswordUpdate
)
from src.transportation.api.dependencies.auth import CurrentUser
from src.transportation.api.dependencies.container import (
    get_get_user_use_case,
    get_update_user_password_use_case,
    get_update_user_phone_use_case
)
from src.domain.use_cases.user.get_user import GetUserUseCase
from src.domain.use_cases.user.update_user_password import UpdateUserPasswordUseCase
from src.domain.use_cases.user.update_user_phone import UpdateUserPhoneUseCase
from src.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    InvalidCredentialsError,
    PasswordStrengthError
)

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def read_current_user(
    current_user: CurrentUser,
    use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)]
):
    """
    Get current logged in user
    """
    try:
        user = use_case.execute(user_id=current_user['user_id'])
        return UserResponse(**user.to_dict())
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    password_data: UserPasswordUpdate,
    current_user: CurrentUser,
    use_case: Annotated[UpdateUserPasswordUseCase, Depends(get_update_user_password_use_case)]
):
    """
    Change password for current user
    """
    try:
        use_case.execute(
            user_id=current_user['user_id'],
            current_password=password_data.password,
            new_password=password_data.new_password
        )
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Error on password change'
        )
    except PasswordStrengthError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/update_phone/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    phone_number: str,
    current_user: CurrentUser,
    use_case: Annotated[UpdateUserPhoneUseCase, Depends(get_update_user_phone_use_case)]
):
    """
    Update phone number for current user
    """
    try:
        use_case.execute(
            user_id=current_user['user_id'],
            phone_number=phone_number
        )
    
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )