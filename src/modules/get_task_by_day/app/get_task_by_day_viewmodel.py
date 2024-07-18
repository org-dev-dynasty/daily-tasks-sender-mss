from datetime import date, time
from typing import Optional, List

from src.shared.domain.entities.task import Task

class TaskViewmodel:
    task_id: str
    task_name: str
    task_date: date
    task_hour: time
    task_description: Optional[str]
    task_local: Optional[str]
    task_status: str

    def __init__(self, task_id: str, task_name: str, task_date: date, task_hour: time, task_description: Optional[str], task_local: Optional[str], task_status: str) -> None:
        self.task_id = task_id
        self.task_name = task_name
        self.task_date = task_date
        self.task_hour = task_hour
        self.task_description = task_description
        self.task_local = task_local
        self.task_status = task_status
    
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

class GetTaskByDayViewmodel:
    tasks_viewmodel_list: List[TaskViewmodel]

    def __init__(self, tasks: List[Task]) -> None:
        tasks_list = []
        for task in tasks:
            task_viewmodel = TaskViewmodel(
                task.task_id,
                task.task_name,
                task.task_date,
                task.task_hour,
                task.task_description,
                task.task_local,
                task.task_status
            )
            tasks_list.append(task_viewmodel)
        
        self.tasks_viewmodel_list = tasks_list

    def to_dict(self):
        tasks_list = []
        for task_viewmodel in self.tasks_viewmodel_list:
            task_viewmodel_to_dict = task_viewmodel.to_dict()
            tasks_list.append(task_viewmodel_to_dict)
        
        return {
            "tasks": tasks_list
        }