"""
Delete User Use Case
Admin-only operation to remove users from the system
"""

from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    PermissionDeniedError
)


class DeleteUserUseCase:
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(
        self,
        user_id: int,
        admin_id: int,
        admin_role: str
    ) -> None:

        # Verify admin role
        if admin_role != 'admin':
            raise PermissionDeniedError("Only admins can delete users")
        
        # Check if user exists
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise EntityNotFoundError(f"User with id {user_id} not found")
        
        # Prevent admin from deleting themselves (safety check)
        if user_id == admin_id:
            raise PermissionDeniedError("Cannot delete your own account")
        
        # Delete user
        deleted = self.user_repository.delete(user_id)
        
        if not deleted:
            raise EntityNotFoundError(f"User with id {user_id} could not be deleted")