import pytest

from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock
from src.modules.create_task.app.create_task_usecase import CreateTaskUsecase
from src.modules.create_task.app.create_task_controller import CreateTaskController

class Test_CreateTaskController:

    def test_create_task_controller(self):
        repo = TaskRepositoryMock()
        usecase = CreateTaskUsecase(repo)
        controller = CreateTaskController(usecase)

        request = HttpRequest(body={
            'task_name': 'prova de os',
            'task_description': 'prova de OS',
            'task_date': '2021-10-10',
            'task_hour': '12:00:00',
            'task_local': 'maua',
            'task_status': 'ACTIVE'
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body['task']['task_name'] == 'prova de os'
        assert response.body['task']['task_date'] == '2021-10-10'
        assert response.body['task']['task_hour'] == '12:00:00'
        assert response.body['task']['task_status'] == 'ACTIVE'
        assert response.body['message'] == 'the task was created'