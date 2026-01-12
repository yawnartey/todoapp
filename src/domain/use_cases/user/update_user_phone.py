# domain/use_cases/user/update_user_phone.py
"""
Update User Phone Number Use Case
Based on: PUT /users/phone_number/{phone_number} endpoint
"""

from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.domain.exceptions.domain_exceptions import EntityNotFoundError


class UpdateUserPhoneUseCase:
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(
        self,
        user_id: int,
        phone_number: str
    ) -> UserEntity:

        # Retrieve user and update phome number
        user = self.user_repository.get_by_id(user_id)
        
        if user is None:
            raise EntityNotFoundError("User", user_id)
        
        user.update_phone_number(phone_number)

        updated_user = self.user_repository.update(user)
    
        return updated_user