from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersController:

    def test_get_all_users_controller(self):
        repo_mock = UserRepositoryMock()
        get_all_users_usecase = GetAllUsersUsecase(repo_mock)
        controller = GetAllUsersController(get_all_users_usecase)

        request = HttpRequest(body={"requester_user": {
            "user_id": repo_mock.users[0].user_id,
            "name": repo_mock.users[0].name,
            "email": repo_mock.users[0].email,
            "phone": repo_mock.users[0].phone,
            "password": repo_mock.users[0].password,
        },
        })

        response = controller.handle(request=request)

        assert response.status_code == 200
        assert len(response.body['users']) == 5
        assert response.body['message'] == 'All users have been retrieved successfully!'
