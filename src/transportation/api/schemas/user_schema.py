# transportation/api/schemas/user_schema.py
"""
User Pydantic schemas for request/response validation
Based on: TodoApp/routers/auth.py (CreateUserRequest) and users.py (UserVerification)
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """
    Schema for user registration
    Based on: CreateUserRequest in auth.py
    """
    username: str = Field(min_length=3)
    email: EmailStr
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=4)
    role: str = Field(default='user')
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    """
    Schema for user response (excludes password)
    """
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserPasswordUpdate(BaseModel):
    """
    Schema for password update
    Based on: UserVerification in users.py
    """
    password: str = Field(description="Current password")
    new_password: str = Field(min_length=4, description="New password")
    
    class Config:
        json_schema_extra = {
            'example': {
                'password': 'OldPass123',
                'new_password': 'NewPass456'
            }
        }


class UserPhoneUpdate(BaseModel):
    """
    Schema for phone number update
    """
    phone_number: str
    
    class Config:
        json_schema_extra = {
            'example': {
                'phone_number': '123-456-7890'
            }
        }