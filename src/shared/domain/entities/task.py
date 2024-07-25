import re
import uuid
import abc
from typing import Optional
from datetime import datetime, date, time

from src.shared.domain.enums.status_enum import STATUS
from src.shared.helpers.errors.domain_errors import EntityError


class Task(abc.ABC):
    task_id: Optional[str]
    user_id: str
    category_id: str
    task_name: str
    task_date: date
    task_hour: time
    task_description: Optional[str]
    task_local: Optional[str]
    task_status: str

    def __init__(
            self,
            task_name: str,
            user_id: str,
            category_id: str,
            task_date: date,
            task_hour: time,
            task_id: Optional[str] = None,
            task_description: Optional[str] = None,
            task_local: Optional[str] = None,
            task_status: str = "ACTIVE"
    ):
        if not task_id:
            self.task_id = uuid.uuid4().hex
        else:
            self.task_id = task_id

        if not user_id:
            raise EntityError("user_id")
        else:
            self.user_id = user_id
        
        if not category_id:
            raise EntityError("category_id")
        else:
            self.category_id = category_id

        if not self.validate_name(task_name):
            raise EntityError("task_name")
        
        if not self.validate_date(task_date):
            raise EntityError("task_date")
        
        if not self.validate_hour(task_hour):
            raise EntityError("task_hour")

        if not self.validate_description(task_description):
            raise EntityError("task_description")

        if not self.validate_local(task_local):
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
    def validate_description(description: str) -> bool:
        if description is None:
            return True
        if len(description) < 2:
            return False
        if description == "":
            return False
        return True

    @staticmethod
    def validate_local(local: str) -> bool:
        if local is None:
            return True
        if len(local) < 2:
            return False
        if local == "":
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
            user_id=task.get("user_id"),
            category_id=task.get("category_id"),
            task_name=task.get("task_name"),
            task_date=task.get("task_date"),
            task_hour=task.get("task_hour"),
            task_description=task.get("task_description"),
            task_local=task.get("task_local"),
            task_status=task.get("task_status")
        )

    def to_dict(self) -> dict:
        return {
            "_id": self.task_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "task_name": self.task_name,
            "task_date": self.task_date,
            "task_hour": self.task_hour,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "task_status": self.task_status
        }