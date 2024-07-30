from src.modules.get_task_by_id.app.get_task_by_id_controller import GetTaskByIdController
from src.modules.get_task_by_id.app.get_task_by_id_usecase import GetTaskByIdUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock


class Test_GetTaskByIdController:

    def test_get_task_by_id_controller(self):
        repo = TaskRepositoryMock()
        usecase = GetTaskByIdUsecase(repo)
        controller = GetTaskByIdController(usecase)
        request = HttpRequest(
            query_params={
                "task_id": repo.tasks[0].task_id
            }, headers={
                'requester_user': {
                    'sub': '1'
                }
            }
        )

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
                "task_id": "1",
                "category": {
                    "category_id": "1",
                    "category_name": "Categoria 1",
                    "category_primary_color": "#123456",
                    "category_secondary_color": "#654321"
                },
                "task_name": "TaskUm",
                "task_date": "2021-12-12",
                "task_hour": "12:00:00",
                "task_description": "Description for task 1",
                "task_local": "Local 1",
                "task_status": "ACTIVE"
            }

    def test_get_task_by_id_controller_with_invalid_task_id(self):
        repo = TaskRepositoryMock()
        usecase = GetTaskByIdUsecase(repo)
        controller = GetTaskByIdController(usecase)
        request = HttpRequest(query_params={}, headers={
            'requester_user': {
                'sub': '1'
            }
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Field task_id is missing'

    def test_get_task_by_id_controller_with_no_items_found(self):
        repo = TaskRepositoryMock()
        usecase = GetTaskByIdUsecase(repo)
        controller = GetTaskByIdController(usecase)
        request = HttpRequest(query_params={"task_id": "123"}, headers={
            'requester_user': {
                'sub': '1'
            }
        })

        response = controller(request)

        assert response.status_code == 404
        assert response.body == 'No items found for task'
