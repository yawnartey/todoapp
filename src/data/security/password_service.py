"""
Password service implementation
Based on: TodoApp/routers/auth.py (bcrypt_context) and TodoApp/validators.py
"""

from passlib.context import CryptContext

from src.domain.interfaces.services.password_service import IPasswordService
from src.domain.exceptions.domain_exceptions import PasswordStrengthError


class PasswordServiceImpl(IPasswordService):
    """Implementation of IPasswordService using passlib/bcrypt"""
    
    def __init__(self):
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    
    def hash_password(self, password: str) -> str:
        """Hash a plain text password using bcrypt"""
        return self.bcrypt_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against hashed password"""
        return self.bcrypt_context.verify(plain_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> str:
        """
        Validate password strength requirements
        """
        errors = []
        
        if len(password) < 4:
            errors.append("Password must be at least 4 characters long")
        
        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not any(char.islower() for char in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit")
        
        if errors:
            raise PasswordStrengthError("; ".join(errors))
        
        return password