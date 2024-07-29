from src.modules.delete_task_by_id.app.delete_task_by_id_controller import DeleteTaskByIdController
from src.modules.delete_task_by_id.app.delete_task_by_id_usecase import DeleteTaskByIdUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock


class Test_DeleteTaskByIdController:

    def test_delete_task_by_id_controller(self):
        repo = TaskRepositoryMock()
        usecase = DeleteTaskByIdUsecase(repo)
        controller = DeleteTaskByIdController(usecase)
        request = HttpRequest(query_params={"task_id": repo.tasks[0].task_id})

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'message': 'Deletada com sucesso'
        }

    def test_Delete_task_by_id_controller_with_invalid_task_id(self):
        repo = TaskRepositoryMock()
        usecase = DeleteTaskByIdUsecase(repo)
        controller = DeleteTaskByIdController(usecase)
        request = HttpRequest(query_params={})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Field task_id is missing'


