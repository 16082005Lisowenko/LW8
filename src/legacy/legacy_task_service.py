"""Модуль для управління задачами (Legacy Refactored)."""
import datetime
import smtplib
from email.mime.text import MIMEText
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Union


class TaskStatus(Enum):
    """Статуси задачі."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    """Сутність задачі."""

    title: str
    user: str
    priority: int
    id: int = 0
    status: TaskStatus = TaskStatus.TODO
    created: str = field(default_factory=lambda: str(datetime.datetime.now()))


class TaskRepository:
    """Клас для зберігання задач у пам'яті."""

    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def save(self, task: Task) -> Task:
        """Зберігає задачу та призначає їй ID."""
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Шукає задачу за ідентифікатором."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


LOG_FILE = "log.txt"
repo = TaskRepository()


def _validate_title(title: str) -> bool:
    """Перевіряє заголовок на валідність."""
    return bool(title and len(title) <= 100)


def _send_email(user_email: str, title: str) -> None:
    """Надсилає email користувачу."""
    try:
        msg = MIMEText(f"New task: {title}")
        msg["Subject"] = "Task created"
        msg["From"] = "noreply@tms.com"
        msg["To"] = user_email
        server = smtplib.SMTP("localhost")
        server.send_message(msg)
        server.quit()
    except smtplib.SMTPException as err:
        print(f"Email error: {err}")


def _log_action(action_msg: str) -> None:
    """Логує дію у файл."""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{datetime.datetime.now()}: {action_msg}\n")


def create_task(title: str, user_email: str, priority: Optional[int] = None) -> Optional[Task]:
    """
    Створює нову задачу.
    Raises нічого не піднімає, повертає None у разі помилки.
    """
    if not _validate_title(title):
        return None
    final_priority = priority if priority is not None else 3
    task = Task(title=title, user=user_email, priority=final_priority)
    repo.save(task)
    _log_action(f"created task {title}")
    _send_email(user_email, title)
    return task


def assign_task(task_id: int, user_email: str) -> Optional[Task]:
    """
    Призначає виконавця задачі.
    Повертає оновлену задачу або None.
    """
    task = repo.get_by_id(task_id)
    if task:
        task.user = user_email
        task.status = TaskStatus.IN_PROGRESS
        _log_action("assigned")
        return task
    return None


def complete_task(task_id: int) -> Union[Task, bool, None]:
    """
    Завершує задачу.
    Повертає Task, False (якщо статус не In Progress) або None.
    """
    task = repo.get_by_id(task_id)
    if not task:
        return None
    if task.status != TaskStatus.IN_PROGRESS:
        return False
    task.status = TaskStatus.DONE
    _log_action("completed")
    return task
