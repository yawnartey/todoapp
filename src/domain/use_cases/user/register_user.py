# domain/use_cases/user/register_user.py
"""
Register User Use Case
Based on: POST /auth/register endpoint
"""

from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.domain.interfaces.services.password_service import IPasswordService
from src.domain.exceptions.domain_exceptions import DuplicateEntityError, PasswordStrengthError


class RegisterUserUseCase:
    """
    Use case: Register a new user
    
    Business flow:
    1. Validate password strength
    2. Check username doesn't already exist
    3. Check email doesn't already exist
    4. Hash password
    5. Create user entity
    6. Validate user data
    7. Save to database
    """
    
    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
    
    def execute(
        self,
        email: str,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        role: str = 'user',
        phone_number: str = None
    ) -> UserEntity:

        # Validate password strength
        validated_password = self.password_service.validate_password_strength(password)
        
        # Check for duplicate username
        if self.user_repository.exists_by_username(username):
            raise DuplicateEntityError("User", "username", username)
        
        # Check for duplicate email
        if self.user_repository.exists_by_email(email):
            raise DuplicateEntityError("User", "email", email)

        hashed_password = self.password_service.hash_password(validated_password)
        
        # Step 5: Create user entity
        user = UserEntity(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            role=role,
            phone_number=phone_number,
            is_active=True
        )
        

        user.validate()
        created_user = self.user_repository.create(user)
        
        return created_user