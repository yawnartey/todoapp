"""
Todo Repository Interface
Defines contract for todo data access
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.todo import TodoEntity


class ITodoRepository(ABC):
    """Interface for todo repository operations"""
    
    @abstractmethod
    def create(self, todo: TodoEntity) -> TodoEntity:
        """Create a new todo"""
        pass
    
    @abstractmethod
    def get_by_id(self, todo_id: int) -> Optional[TodoEntity]:
        """Get todo by ID"""
        pass
    
    @abstractmethod
    def get_by_id_and_owner(self, todo_id: int, owner_id: int) -> Optional[TodoEntity]:
        """Get todo by ID and owner"""
        pass
    
    @abstractmethod
    def get_all_by_owner(self, owner_id: int) -> List[TodoEntity]:
        """Get all todos for a specific owner"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[TodoEntity]:
        """Get all todos (admin operation)"""
        pass
    
    @abstractmethod
    def update(self, todo: TodoEntity) -> TodoEntity:
        """Update existing todo"""
        pass
    
    @abstractmethod
    def delete(self, todo_id: int, owner_id: int) -> bool:
        """Delete todo by ID and owner"""
        pass
    
    @abstractmethod
    def delete_by_id(self, todo_id: int) -> bool:
        """Delete todo by ID (admin operation)"""
        pass