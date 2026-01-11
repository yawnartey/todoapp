"""
Password Service Interface
Defines contract for password hashing and validation
"""

from abc import ABC, abstractmethod


class IPasswordService(ABC):
    """Interface for password operations"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a plain text password"""
        pass
    
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against hashed password"""
        pass
    
    @abstractmethod
    def validate_password_strength(self, password: str) -> str:
        """Validate password meets strength requirements"""
        pass