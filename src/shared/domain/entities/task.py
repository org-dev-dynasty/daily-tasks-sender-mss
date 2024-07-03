import re
import abc
from typing import Optional
from datetime import date, time

from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.domain_errors import EntityError


class Task(abc.ABC):
    task_id: Optional[str]
    task_name: str
    task_date: date
    task_hour: time
    task_description: Optional[str]
    task_local: Optional[str]
    task_status: str

    def __init__(
            self,
            task_id: int,
            task_name: str,
            task_description: str,
            task_local: Optional[str] = None,
            task_status: str = "ACTIVE"
    ):
        if task_id is None:
            self.task_id = None
        else:
            self.task_id = task_id

        if not self.validate_attribute(task_name):
            raise EntityError("task_name")

        if not self.validate_attribute(task_description):
            raise EntityError("task_description")

        if not self.validate_attribute(task_local):
            raise EntityError("task_local")

        if not self.validate_task_status(task_status):
            raise EntityError("task_status")

        self.task_name = task_name
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status

    @staticmethod
    def validate_attribute(name: str) -> bool:
        if name is None:
            return False
        if len(name) < 2:
            return False
        if name == "":
            return False
        if re.search(r'\d', name):
            return False
        return True

    @staticmethod
    def validate_task_status(status: STATUS) -> bool:
        if status is None:
            return False
        if status not in STATUS:
            return False
        return True

    def parse_object(task: dict) -> 'Task':
        return Task(
            task_id=task.get("task_id"),
            task_name=task.get("task_name"),
            task_description=task.get("task_description"),
            task_local=task.get("task_local"),
            task_status=task.get("task_status")
        )

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status
        }
