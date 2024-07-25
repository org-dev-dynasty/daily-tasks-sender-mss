from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.domain.irepositories.category_repository_interface import ICategoryRepository
from src.shared.helpers.errors.domain_errors import EntityError

class CreateTaskUsecase:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo
    
    def __call__(self, task: Task) -> Task:
        if not task.task_name:
            raise EntityError("task_name")
        if not task.user_id:
            raise EntityError("user_id")
        if not task.task_date:
            raise EntityError("task_date")
        if not task.task_hour:
            raise EntityError("task_hour")
        if not task.task_status:
            raise EntityError("task_status")
        if not task.category_id:
            raise EntityError("category_id")
        
        task_response = self.repo.create_task(task)
        return task_response
