from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_CreateUserController:

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        request = HttpRequest(body={
            'name': 'John Doe',
            'email': 'johnretardado@gmail.com',
            'password': 'Teste@01',
            'phone': '11987655142',
            'accepted_terms': True,
            'accepted_notifications_email': True
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body['user']['name'] == 'John Doe'
        assert response.body['user']['email'] == 'johnretardado@gmail.com'
        assert response.body['message'] == 'the user was created'
