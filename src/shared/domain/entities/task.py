import re
import abc
from typing import Optional
from datetime import datetime, date, time

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
            task_name: str,
            task_date: date,
            task_hour: time,
            task_id: Optional[str] = None,
            task_description: Optional[str] = None,
            task_local: Optional[str] = None,
            task_status: str = "ACTIVE"
    ):
        if task_id is None:
            self.task_id = None
        else:
            self.task_id = task_id

        if not self.validate_name(task_name):
            raise EntityError("task_name")
        
        if not self.validate_date(task_date):
            raise EntityError("task_date")
        
        if not self.validate_hour(task_hour):
            raise EntityError("task_hour")

        if not self.validate_attribute(task_description):
            raise EntityError("task_description")

        if not self.validate_attribute(task_local):
            raise EntityError("task_local")

        if not self.validate_task_status(task_status):
            raise EntityError("task_status")

        self.task_name = task_name
        self.task_date = task_date
        self.task_hour = task_hour
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        if len(name) < 2:
            return False
        if name == "":
            return False
        return True
    
    @staticmethod
    def validate_attribute(attribute: str) -> bool:
        if attribute == "":
            return False
        return True
    
    @staticmethod
    def validate_date(datestr: str) -> bool:
        if datestr is None:
            return False
        try:
            datetime.strptime(datestr, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_hour(hour: str) -> bool:
        if hour is None:
            return False
        try:
            datetime.strptime(hour, "%H:%M:%S")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_task_status(status: str) -> bool:
        if status is None:
            return False
        try:
            STATUS(status)
            return True
        except ValueError:
            return False

    def parse_object(task: dict) -> 'Task':
        return Task(
            task_id=task.get("task_id"),
            task_name=task.get("task_name"),
            task_date=task.get("task_date"),
            task_hour=task.get("task_hour"),
            task_description=task.get("task_description"),
            task_local=task.get("task_local"),
            task_status=task.get("task_status")
        )

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_date": self.task_date,
            "task_hour": self.task_hour,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status
        }