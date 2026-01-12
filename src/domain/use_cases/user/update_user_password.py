# domain/use_cases/user/update_user_password.py
"""
Update User Password Use Case
Based on: PUT /users/password endpoint
"""

from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.domain.interfaces.services.password_service import IPasswordService
from src.domain.exceptions.domain_exceptions import EntityNotFoundError, InvalidCredentialsError, PasswordStrengthError


class UpdateUserPasswordUseCase:
    
    
    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
    
    def execute(
        self,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> UserEntity:
        
      # Retrieve user
        user = self.user_repository.get_by_id(user_id)
        
        if user is None:
            raise EntityNotFoundError("User", user_id)

        if not self.password_service.verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsError("Current password is incorrect")

        validated_password = self.password_service.validate_password_strength(new_password)

        new_hashed_password = self.password_service.hash_password(validated_password)

        user.update_password(new_hashed_password)

        updated_user = self.user_repository.update(user)
        
        return updated_user