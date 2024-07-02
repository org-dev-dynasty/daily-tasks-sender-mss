import datetime
import json

from src.shared.domain.observability.observability_interface import IObservability
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.domain.entities.user import User
from .create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, TermsNotAccepted
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created, Forbidden


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase, observability: IObservability) -> None:
        self.createUserUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('access_level') is None:
                raise MissingParameters('access_level')

            if request.data.get('access_level') not in [access_level.value for access_level in ACCESS_LEVEL]:
                raise EntityError('access_level')

            if request.data.get('role') is None:
                raise MissingParameters('role')

            if request.data.get('role') not in [role.value for role in ROLE]:
                raise EntityError('role')

            if request.data.get('accepted_terms') is None:
                raise MissingParameters('accepted_terms')

            # if request.data.get('accepted_notifications_sms') is None:
            #     raise MissingParameters('accepted_notifications_sms')

            if request.data.get('accepted_notifications_email') is None:
                raise MissingParameters('accepted_notifications_email')

            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('password') is None:
                raise MissingParameters('password')

            if request.data.get('certificate_with_social_name') is None:
                raise MissingParameters('certificate_with_social_name')

            phone = request.data.get("phone") if request.data.get("phone") != "" else None

            if phone is not None:
                phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
                phone = phone if phone.startswith('+') else f'+{phone}'

            if request.data.get('accepted_notifications_sms') == True and phone is None:
                raise MissingParameters("phone")

            user_dict = {
                'email': request.data.get('email').replace(' ', ''),
                'name': request.data.get('name'),
                'password': request.data.get('password'),
                'ra': request.data.get('ra').replace('.', '').replace('-', '').replace(' ', '') if request.data.get(
                    'ra') else None,
                'role': request.data.get('role'),
                'access_level': request.data.get('access_level'),
                'created_at': int(datetime.datetime.now().timestamp() * 1000),
                'updated_at': None,
                'social_name': request.data.get('social_name') if request.data.get('social_name') else None,
                'accepted_terms': request.data.get('accepted_terms'),
                'accepted_notifications_sms': False,
                'accepted_notifications_email': request.data.get('accepted_notifications_email'),
                'certificate_with_social_name': request.data.get('certificate_with_social_name'),
                'phone': None,
            }

            new_user = User.parse_object(user_dict)
            created_user = self.createUserUsecase(new_user)

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
