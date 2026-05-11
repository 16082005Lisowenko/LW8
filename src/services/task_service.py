"""Модуль сервісу задач."""
from typing import List
from src.models.task import Task

class TaskService:
    """Сервіс для управління задачами."""
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def create_task(self, title: str, user: str, priority: int) -> Task:
        """Створює нову задачу."""
        task = Task(title=title, user=user, priority=priority)
        self.tasks.append(task)
        return task

    def get_tasks(self) -> List[Task]:
        """Повертає список задач."""
        return self.tasks
