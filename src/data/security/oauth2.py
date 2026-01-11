# data/security/oauth2.py
"""
OAuth2 utilities for FastAPI integration
Based on: TodoApp/routers/auth.py (oauth2_bearer, get_current_user)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.domain.exceptions.domain_exceptions import AuthenticationError
from src.data.security.jwt_service import JWTServiceImpl


# OAuth2 scheme for token extraction from request
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Dependency that extracts and validates current user from JWT token
    
    Returns dict with user_id, username, role
    Raises HTTPException if token is invalid
    """
    try:
        jwt_service = JWTServiceImpl()
        payload = jwt_service.decode_token(token)
        
        return {
            'user_id': payload['user_id'],
            'username': payload['username'],
            'role': payload['role']
        }
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'WWW-Authenticate': 'Bearer'}
        )


def get_current_user_id(current_user: dict = Depends(get_current_user)) -> int:
    """
    Convenience dependency to get just the user ID
    """
    return current_user['user_id']


def get_current_user_role(current_user: dict = Depends(get_current_user)) -> str:
    """
    Convenience dependency to get just the user role
    """
    return current_user['role']


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency that ensures current user is admin
    Raises HTTPException if not admin
    """
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user