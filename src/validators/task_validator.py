from datetime import datetime, timedelta

class TaskValidator:
    def is_title_valid(self, title: str | None) -> bool:
        if not isinstance(title, str) or not title.strip():
            return False
        return len(title.strip()) <= 100

    def is_due_date_valid(self, due_date: datetime | None) -> bool:
        if not isinstance(due_date, datetime):
            return False
        now = datetime.utcnow()
        if due_date < now:
            return False
        if due_date > now + timedelta(days=731):
            return False
        return True

    def is_priority_valid(self, priority: int | None) -> bool:
        if type(priority) is not int: # Використовуємо type(), щоб відсіяти bool (True/False)
            return False
        return 1 <= priority <= 4

    def validate(self, title, due_date, priority) -> list[str]:
        errors = []
        if not self.is_title_valid(title):
            errors.append('Title is invalid or too long (max 100 chars)')
        if not self.is_due_date_valid(due_date):
            errors.append('Due date is invalid, in the past, or too far in the future')
        if not self.is_priority_valid(priority):
            errors.append('Priority must be an integer between 1 and 4')
        return errors
