from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidCredentials

class UpdateTaskStatusUsecase:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo
    
    def execute(self, task_id: str, task_status: str):
        if not task_status:
            return EntityError("Task status is required")
        if Task.validate_task_status(task_status):
            return InvalidCredentials("Invalid task status")
        
        task = self.repo.update_task_status(task_id, task_status)

        return task
