from datetime import date, time
from src.shared.domain.entities.task import Task


class TaskViewmodel:
    task_id: str
    task_name: str
    task_date: date
    task_hour: time
    task_description: str
    task_local: str
    task_status: str

    def __init__(self, task: Task):
        self.task_id = task.task_id
        self.task_name = task.task_name
        self.task_date = task.task_date
        self.task_hour = task.task_hour
        self.task_description = task.task_description
        self.task_local = task.task_local
        self.task_status = task.task_status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_date": self.task_date,
            "task_hour": self.task_hour,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status,
        }


class GetTaskByIdViewmodel:

    def __init__(self, task: Task):
        self.task = TaskViewmodel(task)

    def to_dict(self) -> dict:
        return {
            "task": self.task.to_dict(),
            "message": "the task was retrieved"
        }
