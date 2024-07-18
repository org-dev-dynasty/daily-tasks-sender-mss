import pytest
from src.shared.domain.entities.task import Task
from src.modules.delete_task_by_id.app.delete_task_by_id_usecase import DeleteTaskByIdUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock

class TestDeleteTaskByIdUsecase:

    def test_delete_task_by_id_usecase(self):
        repo_task = TaskRepositoryMock()
        usecase = DeleteTaskByIdUsecase(repo_task)
        len_before = len(repo_task.tasks)

        task_id = "1"
        usecase(task_id) 
        len_after = len_before - 1
        assert len(repo_task.tasks) == len_after
        assert all(task.task_id != task_id for task in repo_task.tasks)

    def test_delete_task_by_id_usecase_with_invalid_task_id(self):
        repo_task = TaskRepositoryMock()
        usecase = DeleteTaskByIdUsecase(repo_task)

        with pytest.raises(EntityError):
            usecase(None)
