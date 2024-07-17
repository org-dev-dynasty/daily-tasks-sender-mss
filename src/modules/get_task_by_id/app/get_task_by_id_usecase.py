from src.shared.domain.entities.task import Task
from src.shared.domain.irepositories.task_repository_interface import ITaskRepository
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetTaskByIdUsecase():
    def __init__(self, task_repo: ITaskRepository):
        self.task_repo = task_repo

    def __call__(self, task_id: int) -> Task:
        if not task_id:
            raise EntityError("Task ID")
        task_response = self.task_repo.get_task_by_id(task_id)
        if not task_response:
            raise NoItemsFound("task")
        return task_response
