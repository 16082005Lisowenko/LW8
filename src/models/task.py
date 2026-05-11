"""Модуль для моделі задачі."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Клас, що описує сутність задачі."""
    title: str
    user: str
    priority: int
    id: int = 0
    status: str = "todo"
    created: str = field(default_factory=lambda: str(datetime.now()))
