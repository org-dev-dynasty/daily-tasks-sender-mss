from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetAllTasksUsecase:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo
    
    def execute(self, user_id: str):
        tasks = self.repo.get_all_tasks(user_id=user_id)

        if len(tasks) == 0:
            raise NoItemsFound("tasks")
        
        return tasks
