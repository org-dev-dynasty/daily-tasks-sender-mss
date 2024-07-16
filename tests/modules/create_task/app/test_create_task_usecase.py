import pytest

from src.shared.domain.entities.task import Task
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock
from src.modules.create_task.app.create_task_usecase import CreateTaskUsecase

class Test_CreateTaskUsecase:

    def test_create_task_usecase(self):
        task = Task(
            task_name="prova de os",
            task_description="prova de OS",
            task_date="2021-10-10",
            task_hour="12:00:00",
            task_local="maua",
            task_status="ACTIVE"
        )
        repo =  TaskRepositoryMock()
        len_before = len(repo.tasks)
        usecase = CreateTaskUsecase(repo)

        new_task = usecase(task)

        assert type(new_task) == Task
        assert new_task.task_name == 'prova de os'
        assert new_task.task_description == 'prova de OS'
        assert new_task.task_status == "ACTIVE"
        assert new_task.task_local == "maua"
        assert len(repo.tasks) == len_before + 1
