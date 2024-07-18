import datetime
import json

from .create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from .create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, TermsNotAccepted
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase) -> None:
        self.createUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('accepted_terms') is None:
                raise MissingParameters('accepted_terms')

            if request.data.get('accepted_notifications_email') is None:
                raise MissingParameters('accepted_notifications_email')

            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('password') is None:
                raise MissingParameters('password')

            phone = request.data.get("phone") if request.data.get("phone") != "" else None

            if phone is not None:
                phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')

            user_dict = {
                'name': request.data.get('name'),
                'email': request.data.get('email').replace(' ', ''),
                'password': request.data.get('password'),
                'phone': phone,
                'accepted_terms': request.data.get('accepted_terms'),
                'accepted_notifications_email': request.data.get('accepted_notifications_email'),
                'created_at': int(datetime.datetime.now().timestamp() * 1000),
            }

            new_user = User.parse_object(user_dict)
            created_user = self.createUserUsecase(new_user)
            
            print('created_user CONTROLLER: ' + str(created_user))
            
            if hasattr(created_user, 'verification_code'):
                viewmodel_with_code = CreateUserViewmodel(created_user, created_user.verification_code)
                resp_with_code = Created(viewmodel_with_code.to_dict())
                return resp_with_code
            viewmodel = CreateUserViewmodel(created_user)
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
