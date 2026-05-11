"""Модуль для моделі задачі."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Перелік всіх можливих статусів задачі."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    ARCHIVED = "archived"


@dataclass
class Task:
    """Клас, що описує сутність задачі."""
    title: str
    user: str = "default"
    priority: int = 1
    id: int = 0
    status: TaskStatus = TaskStatus.TODO
    created: str = field(default_factory=lambda: str(datetime.now()))

    def change_status(self, new_status: TaskStatus):
        """Змінює статус задачі згідно з суворою матрицею переходів."""
        if self.status == new_status:
            raise ValueError("Already in this status")
        
        # Матриця дозволених переходів (згідно з твоїми тестами)
        allowed = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
            TaskStatus.IN_PROGRESS: [TaskStatus.IN_REVIEW, TaskStatus.BLOCKED],
            TaskStatus.IN_REVIEW: [TaskStatus.IN_PROGRESS, TaskStatus.DONE],
            TaskStatus.BLOCKED: [TaskStatus.IN_PROGRESS],
        }

        if new_status not in allowed.get(self.status, []):
            raise ValueError(f"Transition {self.status.name} -> {new_status.name} forbidden")

        self.status = new_status
