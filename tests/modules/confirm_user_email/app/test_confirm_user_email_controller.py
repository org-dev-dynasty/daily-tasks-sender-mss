from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.modules.confirm_user_email.app.confirm_user_email_usecase import ConfirmUserEmailUsecase
from src.modules.confirm_user_email.app.confirm_user_email_controller import ConfirmUserEmailController
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class Test_ConfirmUserEmailController:

    def test_confirm_controller(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserEmailUsecase(repo)
        controller = ConfirmUserEmailController(usecase)
        request = HttpRequest(body={
            'email': 'digao@gmail.com',
            'verification_code': '123456'
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['message'] == 'User email has been confirmed'
