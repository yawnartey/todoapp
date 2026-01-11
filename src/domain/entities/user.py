# domain/entities/user.py
from typing import Optional
from datetime import datetime, timezone
import re


class UserEntity:
    """
    User domain entity - represents a user with business logic
    """
    
    def __init__(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
        role: str = 'user',
        phone_number: Optional[str] = None,
        is_active: bool = True,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.role = role
        self.phone_number = phone_number
        self.is_active = is_active
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
    
    def validate(self) -> None:
        """
        Validate user business rules
        Raises ValueError if validation fails
        """
        errors = []
        
        # Validate username
        if not self.username or not self.username.strip():
            errors.append("Username cannot be empty or whitespace")
        elif len(self.username.strip()) < 3:
            errors.append("Username must be at least 3 characters long")
        
        # Validate email
        if not self.email or not self.email.strip():
            errors.append("Email cannot be empty")
        elif not self._is_valid_email(self.email):
            errors.append("Email format is invalid")
        
        # Validate first name
        if not self.first_name or not self.first_name.strip():
            errors.append("First name cannot be empty or whitespace")
        elif len(self.first_name.strip()) < 3:
            errors.append("First name must be at least 3 characters long")
        
        # Validate last name
        if not self.last_name or not self.last_name.strip():
            errors.append("Last name cannot be empty or whitespace")
        elif len(self.last_name.strip()) < 3:
            errors.append("Last name must be at least 3 characters long")
        
        # Validate role
        valid_roles = ['user', 'admin', 'student']
        if self.role not in valid_roles:
            errors.append(f"Role must be one of: {', '.join(valid_roles)}")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Basic email validation
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def is_admin(self) -> bool:
        """
        Check if user has admin role
        """
        return self.role == 'admin'
    
    def update_phone_number(self, phone_number: str) -> None:
        """
        Update user phone number
        """
        self.phone_number = phone_number
        self.updated_at = datetime.now(timezone.utc)
    
    def update_password(self, new_hashed_password: str) -> None:
        """
        Update user password (already hashed)
        Business rule: Password must be different from current
        """
        if self.hashed_password == new_hashed_password:
            raise ValueError("New password must be different from current password")
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now(timezone.utc)
    
    def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None
    ) -> None:
        """
        Update user profile information
        """
        if first_name is not None:
            if len(first_name.strip()) < 3:
                raise ValueError("First name must be at least 3 characters long")
            self.first_name = first_name
        
        if last_name is not None:
            if len(last_name.strip()) < 3:
                raise ValueError("Last name must be at least 3 characters long")
            self.last_name = last_name
        
        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Email format is invalid")
            self.email = email
        
        if phone_number is not None:
            self.phone_number = phone_number
        
        self.updated_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        """
        Convert entity to dictionary representation
        Note: Excludes hashed_password for security
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'phone_number': self.phone_number,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self) -> str:
        return f"UserEntity(id={self.id}, username='{self.username}', role='{self.role}')"