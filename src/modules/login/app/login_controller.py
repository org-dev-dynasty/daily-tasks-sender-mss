from .login_usecase import LoginUsecase
from .login_viewmodel import LoginViewmodel
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class LoginController:
    def __init__(self, usecase: LoginUsecase):
        self.usecase = usecase

    def handle(self, request: IRequest, email, password):
        try:
            login = self.usecase.execute(email, password)

            print(f'usecase resp: {login}')

            viewmodel = LoginViewmodel(email, password)

            print(f'viewmodel: {viewmodel.to_dict()}')

            return OK(viewmodel.to_dict())

        except NoItemsFound as e:
            return NotFound(str(e))
        except EntityError as e:
            return BadRequest(str(e))
        except Exception as e:
            return InternalServerError(str(e))
