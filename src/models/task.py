from enum import Enum
from dataclasses import dataclass


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    BLOCKED = "blocked"


# Словник дозволених переходів (відповідає нашій матриці)
ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
    TaskStatus.IN_PROGRESS: [TaskStatus.IN_REVIEW, TaskStatus.BLOCKED],
    TaskStatus.IN_REVIEW: [TaskStatus.DONE, TaskStatus.IN_PROGRESS],
    TaskStatus.BLOCKED: [TaskStatus.IN_PROGRESS],
    TaskStatus.DONE: [],
}


@dataclass
class Task:
    title: str
    status: TaskStatus = TaskStatus.TODO

    def change_status(self, new_status: TaskStatus):
        if new_status not in ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(f"Cannot transition from {self.status.name} to {new_status.name}")
        self.status = new_status


x = 1
