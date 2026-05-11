import pytest
from src.models.task import Task, TaskStatus

# Описуємо всі 25 переходів: (from_status, to_status, is_allowed)
TRANSITIONS_MATRIX = [
    # ------------------ З TODO ------------------
    (TaskStatus.TODO, TaskStatus.TODO, False),
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS, True),
    (TaskStatus.TODO, TaskStatus.IN_REVIEW, False),
    (TaskStatus.TODO, TaskStatus.DONE, False),
    (TaskStatus.TODO, TaskStatus.BLOCKED, False),
    # -------------- З IN_PROGRESS ---------------
    (TaskStatus.IN_PROGRESS, TaskStatus.TODO, False),
    (TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS, False),
    (TaskStatus.IN_PROGRESS, TaskStatus.IN_REVIEW, True),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE, False),
    (TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, True),
    # --------------- З IN_REVIEW ----------------
    (TaskStatus.IN_REVIEW, TaskStatus.TODO, False),
    (TaskStatus.IN_REVIEW, TaskStatus.IN_PROGRESS, True),
    (TaskStatus.IN_REVIEW, TaskStatus.IN_REVIEW, False),
    (TaskStatus.IN_REVIEW, TaskStatus.DONE, True),
    (TaskStatus.IN_REVIEW, TaskStatus.BLOCKED, False),
    # ---------------- З BLOCKED -----------------
    (TaskStatus.BLOCKED, TaskStatus.TODO, False),
    (TaskStatus.BLOCKED, TaskStatus.IN_PROGRESS, True),
    (TaskStatus.BLOCKED, TaskStatus.IN_REVIEW, False),
    (TaskStatus.BLOCKED, TaskStatus.DONE, False),
    (TaskStatus.BLOCKED, TaskStatus.BLOCKED, False),
    # ------------------ З DONE ------------------
    (TaskStatus.DONE, TaskStatus.TODO, False),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS, False),
    (TaskStatus.DONE, TaskStatus.IN_REVIEW, False),
    (TaskStatus.DONE, TaskStatus.DONE, False),
    (TaskStatus.DONE, TaskStatus.BLOCKED, False),
]


@pytest.mark.parametrize("from_status, to_status, is_allowed", TRANSITIONS_MATRIX)
def test_task_status_transitions(from_status, to_status, is_allowed):
    # Arrange: створюємо задачу з початковим статусом
    task = Task(title="Test Matrix Task", status=from_status)

    # Act & Assert
    if is_allowed:
        task.change_status(to_status)
        assert task.status == to_status
    else:
        with pytest.raises(ValueError):
            task.change_status(to_status)
