import datetime

from .create_user_oauth_viewmodel import CreateUserOAuthViewmodel
from src.shared.domain.entities.user import User
from .create_user_oauth_usecase import CreateUserOAuthUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, TermsNotAccepted
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created


class CreateUserController:
    def __init__(self, usecase: CreateUserOAuthUsecase) -> None:
        self.CreateUserOAuthUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('email') is None:
                raise MissingParameters('email')

            phone = request.data.get("phone") if request.data.get(
                "phone") != "" else None

            if phone is not None:
                phone = phone.replace(' ', '').replace(
                    '(', '').replace(')', '').replace('-', '')

            user_dict = {
                'name': request.data.get('name'),
                'email': request.data.get('email').replace(' ', ''),
                'phone': phone,
            }

            new_user = User.parse_object(user_dict)
            created_user = self.CreateUserOAuthUsecase(new_user)


            viewmodel = CreateUserOAuthViewmodel(access_token=created_user['access_token'], id_token=created_user['id_token'],
                                                    refresh_token=created_user['refresh_token'])
            response = Created(viewmodel.to_dict())
            return response

        except DuplicatedItem as err:
            return Conflict(
                body=f"Usuário ja cadastrado com esses dados: {err.message}" if err.message != "user" else "Usuário ja cadastrado com esses dados")

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except TermsNotAccepted as err:
            return BadRequest(body="É necessário aceitar os termos de uso para se cadastrar")

        except Exception as err:
            return InternalServerError(body=err.args[0])
