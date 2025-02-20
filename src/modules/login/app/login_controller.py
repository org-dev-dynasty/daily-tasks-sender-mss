from src.shared.helpers.errors.controller_errors import MissingParameters
from .login_usecase import LoginUseCase
from .login_viewmodel import LoginViewmodel
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidCredentials, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, NotFound


class LoginController:
    def __init__(self, usecase: LoginUseCase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('password') is None:
                raise MissingParameters('password')

            data = self.usecase(request.data.get('email'), request.data.get('password'))
            login_user_viewmodel = LoginViewmodel(access_token=data['access_token'], id_token=data['id_token'],
                                                  refresh_token=data['refresh_token'])
            response = OK(body=login_user_viewmodel.to_dict())

            return response

        except NoItemsFound as e:
            return NotFound(body=e.message)
        except ForbiddenAction as e:
            return Forbidden(body=e.message)
        except MissingParameters as e:
            return BadRequest(body=e.message)
        except EntityError as e:
            return BadRequest(body=e.message)
        except InvalidCredentials as e:
            return Forbidden(body=e.message)
        except Exception as e:
            return InternalServerError(body=str(e))