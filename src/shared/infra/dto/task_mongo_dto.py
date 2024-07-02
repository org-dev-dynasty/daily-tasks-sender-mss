from typing import Optional
from datetime import date, time

from src.shared.domain.entities.task import Task

class TaskMongoDTO:
    task_id: Optional[str]
    task_name: str
    task_date: date
    task_hour: time
    task_description: Optional[str]
    task_local: Optional[str]
    task_status: str

    def __init__(self, task_id: Optional[str], task_name: str, task_date: date, task_hour: time, task_description: Optional[str], task_local: Optional[str], task_status: str):
        self.task_id = task_id
        self.task_name = task_name
        self.task_date = task_date
        self.task_hour = task_hour
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status
    
    @staticmethod
    def from_mongo(data) -> "TaskMongoDTO":
        try:
            obj_id = data["_id"]
            task_id = str(obj_id)

            return TaskMongoDTO(
                task_id=task_id,
                task_name=data["task_name"],
                task_date=data["task_date"],
                task_hour=data["task_hour"],
                task_description=data.get("task_description"),
                task_local=data.get("task_local"),
                task_status=data["task_status"]
            )
        except KeyError as e:
            print(f'KeyError: {e} em data: {data}')
            raise
    
    @staticmethod
    def to_entity(self) -> Task:
        return Task(
            task_id=self.task_id,
            task_name=self.task_name,
            task_date=self.task_date,
            task_hour=self.task_hour,
            task_description=self.task_description,
            task_local=self.task_local,
            task_status=self.task_status
        )
    
    @classmethod
    def to_mongo(cls, task: Task):
        return {
            "task_name": task.task_name,
            "task_date": task.task_date,
            "task_hour": task.task_hour,
            "task_description": task.task_description,
            "task_local": task.task_local,
            "task_status": task.task_status
        }
    
    def from_entity(task: Task) -> "TaskMongoDTO":
        return TaskMongoDTO(
            task_id=task.task_id,
            task_name=task.task_name,
            task_date=task.task_date,
            task_hour=task.task_hour,
            task_description=task.task_description,
            task_local=task.task_local,
            task_status=task.task_status
        )