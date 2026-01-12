"""
User repository implementation
Implements IUserRepository interface using SQLAlchemy
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories.user_repository import IUserRepository
from src.data.database.models import UserModel


class UserRepositoryImpl(IUserRepository):
    """SQLAlchemy implementation of IUserRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: UserModel) -> UserEntity:
        """Convert UserModel to UserEntity"""
        return UserEntity(
            id=model.id,
            email=model.email,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            hashed_password=model.hashed_password,
            role=model.role,
            phone_number=model.phone_number,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def create(self, user: UserEntity) -> UserEntity:
        """Create a new user in database"""
        user_model = UserModel(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            role=user.role,
            phone_number=user.phone_number,
            is_active=user.is_active
        )
        
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        
        return self._to_entity(user_model)
    
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Get user by ID"""
        user_model = self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        
        if user_model is None:
            return None
        
        return self._to_entity(user_model)
    
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get user by username"""
        user_model = self.db.query(UserModel).filter(
            UserModel.username == username
        ).first()
        
        if user_model is None:
            return None
        
        return self._to_entity(user_model)
    
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email"""
        user_model = self.db.query(UserModel).filter(
            UserModel.email == email
        ).first()
        
        if user_model is None:
            return None
        
        return self._to_entity(user_model)
    
    def get_all(self) -> List[UserEntity]:
        """Get all users - admin access endpoint"""
        user_models = self.db.query(UserModel).all()
        return [self._to_entity(model) for model in user_models]
    
    def update(self, user: UserEntity) -> UserEntity:
        """Update existing user"""
        user_model = self.db.query(UserModel).filter(
            UserModel.id == user.id
        ).first()
        
        if user_model is None:
            raise ValueError(f"User with id {user.id} not found")
        
        # Update fields
        user_model.email = user.email
        user_model.username = user.username
        user_model.first_name = user.first_name
        user_model.last_name = user.last_name
        user_model.hashed_password = user.hashed_password
        user_model.role = user.role
        user_model.phone_number = user.phone_number
        user_model.is_active = user.is_active
        
        self.db.commit()
        self.db.refresh(user_model)
        
        return self._to_entity(user_model)
    
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        result = self.db.query(UserModel).filter(
            UserModel.id == user_id
        ).delete()
        
        self.db.commit()
        
        return result > 0
    
    def exists_by_username(self, username: str) -> bool:
        """Check if username already exists"""
        return self.db.query(UserModel).filter(
            UserModel.username == username
        ).first() is not None
    
    def exists_by_email(self, email: str) -> bool:
        """Check if email already exists"""
        return self.db.query(UserModel).filter(
            UserModel.email == email
        ).first() is not None