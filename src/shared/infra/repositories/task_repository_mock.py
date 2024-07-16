from typing import List, Optional
from datetime import date, time
from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository

class TaskRepositoryMock(ITaskRepository):
    def __init__(self):
        self.tasks = [
            Task(task_id="1", task_name="TaskUm", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 1", task_local="Local 1", task_status="ACTIVE"),
            Task(task_id="2", task_name="TaskDois", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 2", task_local="Local 2", task_status="ACTIVE"),
            Task(task_id="3", task_name="TaskTres", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 3", task_local="Local 3", task_status="INACTIVE"),
            Task(task_id="4", task_name="TaskQuatro", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 4", task_local="Local 4", task_status="ACTIVE"),
            Task(task_id="5", task_name="TaskCinco", task_hour="12:00:00", task_date="2021-12-12", task_description="Description for task 5", task_local="Local 5", task_status="INACTIVE"),
        ]

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def create_task(self, task: Task) -> Task:
        self.tasks.append(task)
        return task

    # def get_task_by_id(self, task_id: int) -> Optional[Task]:
    #     return next((task for task in self.tasks if task.task_id == task_id), None)

    # def update_task(self, task_id: int, task: Task) -> Optional[Task]:
    #     for i, t in enumerate(self.tasks):
    #         if t.task_id == task_id:
    #             self.tasks[i] = task
    #             return task
    #     return None

    # def delete_task(self, task_id: int) -> bool:
    #     task = self.get_task_by_id(task_id)
    #     if task:
    #         self.tasks.remove(task)
    #         return True
    #     return False
