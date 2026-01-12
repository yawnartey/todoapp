"""
Todo repository implementation
Implements ITodoRepository interface using SQLAlchemy
"""

from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.domain.entities.todo import TodoEntity
from src.domain.interfaces.repositories.todo_repository import ITodoRepository
from src.data.database.models import TodoModel


class TodoRepositoryImpl(ITodoRepository):
    """SQLAlchemy implementation of ITodoRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: TodoModel) -> TodoEntity:
        """Convert TodoModel to TodoEntity"""
        return TodoEntity(
            id=model.id,
            title=model.title,
            description=model.description,
            priority=model.priority,
            complete=model.complete,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: TodoEntity) -> TodoModel:
        """Convert TodoEntity to TodoModel"""
        return TodoModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            priority=entity.priority,
            complete=entity.complete,
            owner_id=entity.owner_id
        )
    
    def create(self, todo: TodoEntity) -> TodoEntity:
        """Create a new todo in database"""
        todo_model = TodoModel(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            complete=todo.complete,
            owner_id=todo.owner_id
        )
        
        self.db.add(todo_model)
        self.db.commit()
        self.db.refresh(todo_model)
        
        return self._to_entity(todo_model)
    
    def get_by_id(self, todo_id: int) -> Optional[TodoEntity]:
        """Get todo by ID"""
        todo_model = self.db.query(TodoModel).filter(
            TodoModel.id == todo_id
        ).first()
        
        if todo_model is None:
            return None
        
        return self._to_entity(todo_model)
    
    def get_by_id_and_owner(self, todo_id: int, owner_id: int) -> Optional[TodoEntity]:
        """Get todo by ID and owner_id"""
        todo_model = self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id
        ).first()
        
        if todo_model is None:
            return None
        
        return self._to_entity(todo_model)
    
    def get_all_by_owner(self, owner_id: int) -> List[TodoEntity]:
        """Get all todos for a specific owner"""
        todo_models = self.db.query(TodoModel).filter(
            TodoModel.owner_id == owner_id
        ).all()
        
        return [self._to_entity(model) for model in todo_models]
    
    def get_all(self) -> List[TodoEntity]:
        """Get all todos - admin access operation"""
        todo_models = self.db.query(TodoModel).all()
        return [self._to_entity(model) for model in todo_models]
    
    def update(self, todo: TodoEntity) -> TodoEntity:
        """Update existing todo"""
        todo_model = self.db.query(TodoModel).filter(
            TodoModel.id == todo.id
        ).first()
        
        if todo_model is None:
            raise ValueError(f"Todo with id {todo.id} not found")
        
        # Update fields
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete
        
        self.db.commit()
        self.db.refresh(todo_model)
        
        return self._to_entity(todo_model)
    
    def delete(self, todo_id: int, owner_id: int) -> bool:
        """Delete todo by ID and owner_id"""
        result = self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id
        ).delete()
        
        self.db.commit()
        
        return result > 0
    
    def delete_by_id(self, todo_id: int) -> bool:
        """Delete todo by ID - admin access operation"""
        result = self.db.query(TodoModel).filter(
            TodoModel.id == todo_id
        ).delete()
        
        self.db.commit()
        
        return result > 0