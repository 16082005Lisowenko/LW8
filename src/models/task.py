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
