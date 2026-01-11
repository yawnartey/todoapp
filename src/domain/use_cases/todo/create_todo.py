# domain/use_cases/todo/create_todo.py
"""
Create Todo Use Case
Based on: POST /todos endpoint
"""

from src.domain.entities.todo import TodoEntity
from src.domain.interfaces.repositories.todo_repository import ITodoRepository


class CreateTodoUseCase:
    
    def __init__(self, todo_repository: ITodoRepository):
        self.todo_repository = todo_repository
    
    def execute(
        self,
        title: str,
        description: str,
        priority: int,
        owner_id: int
    ) -> TodoEntity:
        
        # Create entity
        todo = TodoEntity(
            title=title,
            description=description,
            priority=priority,
            complete=False,
            owner_id=owner_id
        )
        
        todo.validate()
        created_todo = self.todo_repository.create(todo)
        
        return created_todo