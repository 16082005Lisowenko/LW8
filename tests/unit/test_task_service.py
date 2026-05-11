"""Тести для TaskService."""
from src.services.task_service import TaskService

def test_create_task_happy_path() -> None:
    """Тест успішного створення задачі."""
    service = TaskService()
    task = service.create_task("Зробити лабу", "student@test.com", 1)
    assert task.title == "Зробити лабу"
    assert task.user == "student@test.com"
    assert len(service.get_tasks()) == 1

def test_get_tasks_happy_path() -> None:
    """Тест отримання списку задач."""
    service = TaskService()
    assert len(service.get_tasks()) == 0
    service.create_task("Тест 1", "test@test.com", 1)
    assert len(service.get_tasks()) == 1
