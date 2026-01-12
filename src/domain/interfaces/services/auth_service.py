"""
Authentication Service Interface
Defines contract for JWT token operations
"""

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Dict, Any


class IAuthService(ABC):
    """Interface for authentication operations"""
    
    @abstractmethod
    def create_access_token(
        self,
        username: str,
        user_id: int,
        role: str,
        expires_delta: timedelta
    ) -> str:
        """Create JWT access token"""
        pass
    
    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate JWT token"""
        pass