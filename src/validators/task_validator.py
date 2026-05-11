"""Модуль валідації задач."""
from datetime import datetime, timedelta


class TaskValidator:
    """Клас-валідатор для перевірки параметрів задачі."""

    def is_title_valid(self, title: str) -> bool:
        """Перевіряє заголовок (не порожній та до 100 символів)."""
        if not title or not title.strip():
            return False
        return len(title) <= 100

    def is_due_date_valid(self, due_date: datetime) -> bool:
        """Перевіряє дату виконання."""
        if due_date is None:
            return False
        now = datetime.now()
        if due_date < now:
            return False
        if due_date > now + timedelta(days=365):
            return False
        return True

    def is_priority_valid(self, priority: int) -> bool:
        """Перевіряє пріоритет (згідно з тестами допустимо 1-4)."""
        return isinstance(priority, int) and 1 <= priority <= 4

    def validate(self, title: str, due_date: datetime, priority: int) -> list:
        """Виконує повну перевірку."""
        errors = []
        if not self.is_title_valid(title):
            errors.append("Invalid title")
        if not self.is_due_date_valid(due_date):
            errors.append("Invalid due date")
        if not self.is_priority_valid(priority):
            errors.append("Invalid priority")
        return errors
