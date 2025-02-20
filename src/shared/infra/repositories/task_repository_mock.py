from typing import List, Optional
from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from datetime import date, time

class TaskRepositoryMock(ITaskRepository):
    def __init__(self):
        self.tasks = [
            Task(task_id="1", user_id="1", category_id="1", task_name="TaskUm", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 1", task_local="Local 1", task_status="ACTIVE"),
            Task(task_id="2", user_id="2", category_id="2", task_name="TaskDois", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 2", task_local="Local 2", task_status="ACTIVE"),
            Task(task_id="3", user_id="3", category_id="3", task_name="TaskTres", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 3", task_local="Local 3", task_status="INACTIVE"),
            Task(task_id="4", user_id="4", category_id="4", task_name="TaskQuatro", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 4", task_local="Local 4", task_status="ACTIVE"),
            Task(task_id="5", user_id="5", category_id="5", task_name="TaskCinco", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 5", task_local="Local 5", task_status="INACTIVE"),
        ]

    def get_all_tasks(self, user_id: str) -> List[Task]:
        return [task for task in self.tasks if task.user_id == user_id]    
    
    def get_all_inactives_tasks(self, user_id: str) -> List[Task]:
        return [task for task in self.tasks if task.task_status == "INACTIVE" and task.user_id == user_id]

    def create_task(self, task: Task) -> Task:
        self.tasks.append(task)
        return task

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        task = {
                "task_id": "1",
                "category": {
                    "category_id": "1",
                    "category_name": "Categoria 1",
                    "category_primary_color": "#123456",
                    "category_secondary_color": "#654321"
                },
                "task_name": "TaskUm",
                "task_date": "2021-12-12",
                "task_hour": "12:00:00",
                "task_description": "Description for task 1",
                "task_local": "Local 1",
                "task_status": "ACTIVE"
            },
        # return next((task for task in self.tasks if task.task_id == task_id), None)
        return task

    def update_task(self, task_id: str, category_id: str, task_name: Optional[str], task_date: Optional[date], task_hour: Optional[time], task_description: Optional[str], task_local: Optional[str], task_status: Optional[str]) -> Task:
        task = self.get_task_by_id(task_id)
        if task_name:
            task.task_name = task_name
        if category_id:
            task.category_id = category_id
        if task_date:
            task.task_date = task_date
        if task_hour:
            task.task_hour = task_hour
        if task_description:
            task.task_description = task_description
        if task_local:
            task.task_local = task_local
        if task_status:
            task.task_status = task_status
        return task

    def delete_task_by_id(self, task_id: str) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def get_task_by_day(self, task_date: date) -> List[Task]:
        return [task for task in self.tasks if task.task_date == task_date]
