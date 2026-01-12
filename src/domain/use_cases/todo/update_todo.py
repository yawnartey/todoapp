# domain/use_cases/todo/update_todo.py
"""
Update Todo Use Case
Based on: PUT /todos/{todo_id} endpoint
"""

from typing import Optional
from src.domain.entities.todo import TodoEntity
from src.domain.interfaces.repositories.todo_repository import ITodoRepository
from src.domain.exceptions.domain_exceptions import EntityNotFoundError, PermissionDeniedError


class UpdateTodoUseCase:

    def __init__(self, todo_repository: ITodoRepository):
        self.todo_repository = todo_repository
    
    def execute(
        self,
        todo_id: int,
        user_id: int,
        user_role: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        complete: Optional[bool] = None
    ) -> TodoEntity:

        # Step 1: Retrieve todo
        todo = self.todo_repository.get_by_id(todo_id)
        
        if todo is None:
            raise EntityNotFoundError("Todo", todo_id)
        
        if not todo.can_be_modified_by(user_id, user_role):
            raise PermissionDeniedError("You don't have permission to modify this todo")
        
        todo.update_details(
            title=title,
            description=description,
            priority=priority,
            complete=complete
        )
        updated_todo = self.todo_repository.update(todo)
        
        return updated_todo