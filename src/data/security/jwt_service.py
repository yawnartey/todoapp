"""
JWT service implementation
Based on: TodoApp/routers/auth.py (create_access_token, decode_token)
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from jose import JWTError, jwt

from src.domain.interfaces.services.auth_service import IAuthService
from src.domain.exceptions.domain_exceptions import AuthenticationError
from src.data.config.settings import get_settings


class JWTServiceImpl(IAuthService):
    """Implementation of IAuthService using python-jose"""
    
    def __init__(self):
        settings = get_settings()
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
    
    def create_access_token(
        self,
        username: str,
        user_id: int,
        role: str,
        expires_delta: timedelta
    ) -> str:
        """Create JWT access token"""
        expire = datetime.now(timezone.utc) + expires_delta
        
        to_encode = {
            'sub': username,
            'id': user_id,
            'role': role,
            'exp': expire
        }
        
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token
        
        Returns payload dict with username, user_id, role
        Raises AuthenticationError if token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            role: str = payload.get('role')
            
            if username is None or user_id is None:
                raise AuthenticationError("Invalid token: missing required claims")
            
            return {
                'username': username,
                'user_id': user_id,
                'role': role
            }
            
        except JWTError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")