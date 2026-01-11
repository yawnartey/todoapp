# transportation/api/dependencies/auth.py
"""
Authentication dependencies for FastAPI
Based on: TodoApp/routers/auth.py (get_current_user)
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.domain.exceptions.domain_exceptions import AuthenticationError
from src.data.security.jwt_service import JWTServiceImpl


# OAuth2 scheme - tells FastAPI where to get the token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:

    try:
        jwt_service = JWTServiceImpl()
        payload = jwt_service.decode_token(token)
        
        return {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'role': payload['role']
        }
        
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )


def get_current_user_id(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> int:
    return current_user['user_id']


def get_current_user_role(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> str:
    return current_user['role']


def require_admin(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin privileges required'
        )
    return current_user


# some route signatures
CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser = Annotated[dict, Depends(require_admin)]