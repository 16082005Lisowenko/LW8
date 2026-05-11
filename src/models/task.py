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
        """Змінює статус задачі з перевіркою правил переходу."""
        if self.status == new_status:
            raise ValueError("Already in this status")
        
        # Логіка заборони переходів із термінальних станів
        if self.status in [TaskStatus.DONE, TaskStatus.CANCELLED]:
            raise ValueError(f"Cannot change status from {self.status.name}")

        # Специфічне правило: з TODO не можна в DONE без перевірки (приклад)
        if self.status == TaskStatus.TODO and new_status == TaskStatus.DONE:
            raise ValueError("Cannot jump from TODO to DONE")

        self.status = new_status
