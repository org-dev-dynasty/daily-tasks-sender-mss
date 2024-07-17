import pytest

from src.shared.domain.entities.task import Task
from src.modules.get_task_by_id.app.get_task_by_id_usecase import GetTaskByIdUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock

class Test_GetTaskByIdUsecase:

    def test_get_task_by_id_usecase(self):
        repo = TaskRepositoryMock()
        usecase = GetTaskByIdUsecase(repo)
        
        task = usecase(task_id=repo.tasks[0].task_id)
        
        assert task.task_id == repo.tasks[0].task_id
        
    def test_get_task_by_id_usecase_with_invalid_task_id(self):
        repo = TaskRepositoryMock()
        usecase = GetTaskByIdUsecase(repo)
        
        with pytest.raises(EntityError):
            usecase(task_id=0)
            
    def test_get_task_by_id_usecase_with_no_items_found(self):
        repo = TaskRepositoryMock()
        usecase = GetTaskByIdUsecase(repo)
        
        with pytest.raises(NoItemsFound):
            usecase(task_id="123")
