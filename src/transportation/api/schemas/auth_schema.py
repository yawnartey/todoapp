# transportation/api/schemas/auth_schema.py
"""
Authentication Pydantic schemas
Based on: TodoApp/routers/auth.py (Token class)
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for JWT token response
    Based on: Token in auth.py
    """
    access_token: str
    token_type: str
    
    class Config:
        json_schema_extra = {
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                'token_type': 'bearer'
            }
        }


class TokenData(BaseModel):
    """
    Schema for decoded token data
    """
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None