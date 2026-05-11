from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Task:
    id: int
    title: str
    priority: int
    due_date: datetime
    creator_id: int
    assignee_id: Optional[int] = None
    status: str = "TODO"

class TaskRepository:
    """Абстракція репозиторію (БД)"""
    def save(self, task: Task) -> Task: pass
    def get_by_id(self, task_id: int) -> Optional[Task]: pass
    def get_by_assignee(self, assignee_id: int) -> List[Task]: pass
    def update(self, task: Task) -> Task: pass

class NotificationService:
    """Абстракція сервісу сповіщень"""
    def send_assignment_notification(self, task_id: int, assignee_id: int) -> None: pass
    def send_status_change_notification(self, task_id: int, new_status: str) -> None: pass

class TaskService:
    def __init__(self, repo: TaskRepository, notifier: NotificationService):
        self.repo = repo
        self.notifier = notifier

    def create_task(self, title: str, priority: int, due_date: datetime, creator_id: int) -> Task:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        task = Task(id=0, title=title, priority=priority, due_date=due_date, creator_id=creator_id)
        return self.repo.save(task)

    def assign_task(self, task_id: int, assignee_id: int) -> Task:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.assignee_id = assignee_id
        updated_task = self.repo.update(task)
        self.notifier.send_assignment_notification(task_id, assignee_id)
        return updated_task

    def get_tasks_by_assignee(self, assignee_id: int) -> List[Task]:
        if assignee_id <= 0:
            raise ValueError("Invalid assignee ID")
        return self.repo.get_by_assignee(assignee_id)

    def change_status(self, task_id: int, new_status: str) -> Task:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        valid_statuses = ["TODO", "IN_PROGRESS", "DONE"]
        if new_status not in valid_statuses:
            raise ValueError("Invalid status")
            
        task.status = new_status
        updated_task = self.repo.update(task)
        self.notifier.send_status_change_notification(task_id, new_status)
        return updated_task
        
    def archive_task(self, task_id: int) -> bool:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if task.status != "DONE":
            raise ValueError("Only DONE tasks can be archived")
        
        task.status = "ARCHIVED"
        self.repo.update(task)
        return True
