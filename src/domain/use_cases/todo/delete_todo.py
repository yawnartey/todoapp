# domain/use_cases/todo/delete_todo.py
"""
Delete Todo Use Case
Based on: DELETE /todos/{todo_id} endpoint
"""

from src.domain.interfaces.repositories.todo_repository import ITodoRepository
from src.domain.exceptions.domain_exceptions import EntityNotFoundError, PermissionDeniedError


class DeleteTodoUseCase:
    
    def __init__(self, todo_repository: ITodoRepository):
        self.todo_repository = todo_repository
    
    def execute(
        self,
        todo_id: int,
        user_id: int,
        user_role: str
    ) -> bool:
        
        todo = self.todo_repository.get_by_id(todo_id)
        
        if todo is None:
            raise EntityNotFoundError("Todo", todo_id)

        if not todo.can_be_deleted_by(user_id, user_role):
            raise PermissionDeniedError("You don't have permission to delete this todo")

        if user_role == 'admin':
            return self.todo_repository.delete_by_id(todo_id)
        else:
            return self.todo_repository.delete(todo_id, user_id)