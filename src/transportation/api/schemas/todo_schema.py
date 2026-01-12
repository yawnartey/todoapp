# transportation/api/schemas/todo_schema.py
"""
Todo Pydantic schemas for request/response validation
Based on: TodoApp/routers/todos.py (TodoRequest class)
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """
    Schema for creating a new todo
    Based on: TodoRequest in todos.py
    """
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=500)
    priority: int = Field(ge=1, le=5)
    complete: bool = False
    
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Buy groceries',
                'description': 'Milk, eggs, bread, butter',
                'priority': 3,
                'complete': False
            }
        }


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo
    All fields optional - only update what's provided
    """
    title: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = Field(default=None, min_length=3, max_length=500)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    complete: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'Buy more groceries',
                'description': 'Milk, eggs, bread, butter, cheese',
                'priority': 4,
                'complete': True
            }
        }


class TodoResponse(BaseModel):
    """
    Schema for todo response
    """
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Allows converting from ORM models/entities