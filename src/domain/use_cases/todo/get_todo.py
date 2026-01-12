# domain/use_cases/todo/get_todo.py
"""
Get Todo Use Case
Based on: GET /todos/{todo_id} endpoint
"""

from src.domain.entities.todo import TodoEntity
from src.domain.interfaces.repositories.todo_repository import ITodoRepository
from src.domain.exceptions.domain_exceptions import EntityNotFoundError, PermissionDeniedError


class GetTodoUseCase:

    def __init__(self, todo_repository: ITodoRepository):
        self.todo_repository = todo_repository
    
    def execute(
        self,
        todo_id: int,
        user_id: int,
        user_role: str
    ) -> TodoEntity:
        
        # Retrieve todo
        todo = self.todo_repository.get_by_id(todo_id)
        
        if todo is None:
            raise EntityNotFoundError("Todo", todo_id)
        
        if not todo.can_be_modified_by(user_id, user_role):
            raise PermissionDeniedError("You don't have permission to view this todo")
        
        return todo