# domain/entities/todo.py
from typing import Optional
from datetime import datetime, timezone


class TodoEntity:
    """
    Todo domain entity - represents a todo item with business logic
    """
    
    def __init__(
        self,
        title: str,
        description: str,
        priority: int,
        complete: bool = False,
        id: Optional[int] = None,
        owner_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.complete = complete
        self.owner_id = owner_id
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
    
    def validate(self) -> None:
        """
        Validate todo business rules
        Raises ValueError if validation fails
        """
        errors = []
        
        # Validate title
        if not self.title or not self.title.strip():
            errors.append("Title cannot be empty or whitespace")
        elif len(self.title.strip()) < 3:
            errors.append("Title must be at least 3 characters long")
        
        # Validate description
        if not self.description or not self.description.strip():
            errors.append("Description cannot be empty or whitespace")
        elif len(self.description.strip()) < 3:
            errors.append("Description must be at least 3 characters long")
        elif len(self.description) > 500:
            errors.append("Description cannot exceed 500 characters")
        
        # Validate priority
        if not isinstance(self.priority, int):
            errors.append("Priority must be an integer")
        elif not (1 <= self.priority <= 5):
            errors.append("Priority must be between 1 and 5")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def mark_complete(self) -> None:
        """
        Mark todo as complete
        Business rule: Cannot mark already completed todo
        """
        if self.complete:
            raise ValueError("Todo is already marked as complete")
        self.complete = True
        self.updated_at = datetime.now(timezone.utc)
    
    def mark_incomplete(self) -> None:
        """
        Mark todo as incomplete
        Business rule: Cannot mark already incomplete todo
        """
        if not self.complete:
            raise ValueError("Todo is already marked as incomplete")
        self.complete = False
        self.updated_at = datetime.now(timezone.utc)
    
    def update_details(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        complete: Optional[bool] = None
    ) -> None:
        """
        Update todo details
        Only updates provided fields
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            if not (1 <= priority <= 5):
                raise ValueError("Priority must be between 1 and 5")
            self.priority = priority
        if complete is not None:
            self.complete = complete
        
        self.updated_at = datetime.utcnow()
    
    def can_be_modified_by(self, user_id: int, user_role: str) -> bool:
        """
        Business rule: Only owner or admin can modify todo
        """
        return self.owner_id == user_id or user_role == 'admin'
    
    def can_be_deleted_by(self, user_id: int, user_role: str) -> bool:
        """
        Business rule: Only owner or admin can delete todo
        """
        return self.owner_id == user_id or user_role == 'admin'
    
    def to_dict(self) -> dict:
        """
        Convert entity to dictionary representation
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'complete': self.complete,
            'owner_id': self.owner_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self) -> str:
        return f"TodoEntity(id={self.id}, title='{self.title}', owner_id={self.owner_id})"