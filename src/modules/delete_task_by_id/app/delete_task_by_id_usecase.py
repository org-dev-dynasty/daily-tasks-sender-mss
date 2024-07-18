from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.helpers.errors.domain_errors import EntityError

class DeleteTaskByIdUsecase:
    def __init__(self, task_repo: ITaskRepository):
        self.task_repo = task_repo

    def __call__(self, task_id: str) -> None:
        if not task_id:
            raise EntityError("Task ID")
        try:
            self.task_repo.delete_task_by_id(task_id)
        except Exception as e:
            raise EntityError("Task") from e
