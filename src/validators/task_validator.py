"""Модуль валідації задач."""
from datetime import datetime, timedelta

class TaskValidator:
    """Клас-валідатор для перевірки параметрів задачі."""

    def is_title_valid(self, title: str) -> bool:
        """Перевіряє, чи валідний заголовок (не порожній)."""
        return bool(title and title.strip())

    def is_due_date_valid(self, due_date: datetime) -> bool:
        """Перевіряє, чи дата виконання в межах норми (від сьогодні до 1 року)."""
        now = datetime.now()
        if due_date < now:
            return False
        if due_date > now + timedelta(days=365):
            return False
        return True

    def is_priority_valid(self, priority: int) -> bool:
        """Перевіряє, чи коректний пріоритет (від 1 до 5)."""
        return isinstance(priority, int) and 1 <= priority <= 5

    def validate(self, title: str, due_date: datetime, priority: int) -> list:
        """Виконує повну перевірку та повертає список помилок."""
        errors = []
        if not self.is_title_valid(title):
            errors.append("Invalid title")
        if not self.is_due_date_valid(due_date):
            errors.append("Invalid due date")
        if not self.is_priority_valid(priority):
            errors.append("Invalid priority")
        return errors
