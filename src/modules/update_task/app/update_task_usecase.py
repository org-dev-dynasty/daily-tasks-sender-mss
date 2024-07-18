from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.domain.entities.task import Task

class UpdateTaskUsecase:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def execute(self, task_id: str, task_name: str, task_date: str, task_hour: str, task_description: str, task_local: str, task_status: str):
        if not task_name is None:
            if not Task.validate_name(task_name):
                raise ValueError("Invalid task name")
        if not task_date is None:
            if not Task.validate_date(task_date):
                raise ValueError("Invalid task date")
        if not task_hour is None:
            if not Task.validate_hour(task_hour):
                raise ValueError("Invalid task hour")
        if not task_status is None:
            if not Task.validate_status(task_status):
                raise ValueError("Invalid task status")
        if not Task.validate_description(task_description):
            raise ValueError("Invalid task description")
        if not Task.validate_local(task_local):
            raise ValueError("Invalid task local")
        
        result = self.repo.update_task(task_id, task_name, task_date, task_hour, task_description, task_local, task_status)
        return result
    