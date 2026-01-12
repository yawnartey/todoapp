# domain/use_cases/user/authenticate_user.py
"""
Authenticate User Use Case
Based on: POST /auth/token endpoint
"""

from datetime import timedelta
from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.domain.interfaces.services.password_service import IPasswordService
from src.domain.interfaces.services.auth_service import IAuthService
from src.domain.exceptions.domain_exceptions import InvalidCredentialsError, InactiveUserError


class AuthenticateUserUseCase:
    
    def __init__(
        self,
        user_repository: IUserRepository,
        password_service: IPasswordService,
        auth_service: IAuthService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.auth_service = auth_service
    
    def execute(
        self,
        username: str,
        password: str,
        token_expires_minutes: int = 20
    ) -> dict:

        user = self.user_repository.get_by_username(username)
        
        if user is None:
            raise InvalidCredentialsError()

        if not self.password_service.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        
        if not user.is_active:
            raise InactiveUserError()
        
        access_token = self.auth_service.create_access_token(
            username=user.username,
            user_id=user.id,
            role=user.role,
            expires_delta=timedelta(minutes=token_expires_minutes)
        )
        
        # Step 5: Return token
        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }