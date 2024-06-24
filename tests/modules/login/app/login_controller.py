from src.modules.login.app.login_controller import LoginController
from src.modules.login.app.login_usecase import LoginUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user.user_repository_mock import UserRepositoryMock


class Test_LoginController:

    def test_login_controller(self):
        repo_mock = UserRepositoryMock()
        login_usecase = LoginUsecase(repo_mock)
        controller = LoginController(login_usecase)

        request = HttpRequest(body={"requester_user": {
            "email": repo_mock.users[0].email,
            "password": repo_mock.users[0].password
        },
        })

        response = controller.handle(request=request, email=repo_mock.users[0].email, password=repo_mock.users[0].password)

        assert response.status_code == 200
