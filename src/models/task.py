"""Модуль для моделі задачі."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Перелік можливих статусів задачі."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    """Клас, що описує сутність задачі."""
    title: str
    user: str
    priority: int
    id: int = 0
    status: TaskStatus = TaskStatus.TODO
    created: str = field(default_factory=lambda: str(datetime.now()))
