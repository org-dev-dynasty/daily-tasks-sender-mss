import pytest

from src.modules.update_task.app.update_task_controller import UpdateTaskController
from src.modules.update_task.app.update_task_usecase import UpdateTaskUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock


class Test_UpdateTaskController:

    def test_update_task_controller(self):
        repo = TaskRepositoryMock()
        usecase = UpdateTaskUsecase(repo)
        controller = UpdateTaskController(usecase)
        request = HttpRequest(
            body={
                "task_id": repo.tasks[0].task_id,
                "task_name": "TaskUm",
                "task_date": "2021-12-12",
                "task_hour": "12:00:00",
                "task_description": "Description for task 1",
                "task_local": "Local 1",
                "task_status": "ACTIVE"
            }
        )

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'message': 'task updated'
        }