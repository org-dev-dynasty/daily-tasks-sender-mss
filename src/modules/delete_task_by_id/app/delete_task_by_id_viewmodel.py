from datetime import date, time
from src.shared.domain.entities.task import Task


class DeleteTaskByIdViewmodel:

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        return {
            "message": "the task was deleted successfully"
        }
