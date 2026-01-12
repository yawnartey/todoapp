"""
User Repository Interface
Defines contract for user data access
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.user import UserEntity


class IUserRepository(ABC):
    """Interface for user repository operations"""
    
    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[UserEntity]:
        """Get all users (admin operation)"""
        pass
    
    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        """Update existing user"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Check if username exists"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if email exists"""
        pass