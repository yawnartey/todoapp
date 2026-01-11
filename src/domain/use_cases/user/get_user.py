# domain/use_cases/user/get_user.py
"""
Get User Use Case
Based on: GET /users endpoint (get current user)
"""

from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.domain.exceptions.domain_exceptions import EntityNotFoundError


class GetUserUseCase:
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> UserEntity:

        # Retrieve user
        user = self.user_repository.get_by_id(user_id)
        
        if user is None:
            raise EntityNotFoundError("User", user_id)
        
        return user