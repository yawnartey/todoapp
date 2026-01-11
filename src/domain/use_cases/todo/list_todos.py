# domain/use_cases/todo/list_todos.py
"""
List Todos Use Case
Based on: GET /todos endpoint
"""

from typing import List
from src.domain.entities.todo import TodoEntity
from src.domain.interfaces.repositories.todo_repository import ITodoRepository


class ListTodosUseCase:
    
    def __init__(self, todo_repository: ITodoRepository):
        self.todo_repository = todo_repository
    
    def execute(
        self,
        user_id: int,
        user_role: str
    ) -> List[TodoEntity]:

        if user_role == 'admin':
            return self.todo_repository.get_all()

        return self.todo_repository.get_all_by_owner(user_id)