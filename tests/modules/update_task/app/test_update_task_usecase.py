import pytest

from src.modules.update_task.app.update_task_usecase import UpdateTaskUsecase
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock

class Test_UpdateTaskByIdViewmodel:

    def test_update_task_usecase(self):
        repo = TaskRepositoryMock()
        usecase = UpdateTaskUsecase(repo)

        task_id = "1"
        task_name = "TaskUm"

        usecase.execute(
            task_id=task_id,
            category_id=repo.tasks[0].category_id,
            task_name=task_name,
            task_date="2021-12-12",
            task_hour="12:00:00",
            task_description="Description for task 1",
            task_local="Local 1",
            task_status="ACTIVE"
        )
        
        assert repo.tasks[0].task_name == task_name

    def test_update_task_usecase_with_invalid_task_id(self):
        repo = TaskRepositoryMock()
        usecase = UpdateTaskUsecase(repo)

        task_id = "100"
        task_name = "TaskUm"

        with pytest.raises(Exception) as exc:
            usecase.execute(
                task_id=task_id,
                category_id=repo.tasks[0].category_id,
                task_name=task_name,
                task_date="2021-12-12",
                task_hour="12:00:00",
                task_description="Description for task 1",
                task_local="Local 1",
                task_status="ACTIVE"
            )

        assert str(exc.value) == "'NoneType' object has no attribute 'task_name'"
