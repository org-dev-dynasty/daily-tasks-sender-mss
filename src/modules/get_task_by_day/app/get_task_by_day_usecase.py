from datetime import date
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository

class GetTaskByDayUsecase:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo
    
    def execute(self, task_date: date):
        if not task_date:
            raise EntityError("Task date is required")
        
        task_response = self.repo.get_task_by_day(task_date)
        if not task_response:
            raise NoItemsFound("task")
        return task_response