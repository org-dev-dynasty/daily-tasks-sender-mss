import datetime

from .load_task_open_ai_viewmodel import LoadTaskOpenAiViewodel
from src.shared.domain.entities.user import User
from .load_task_open_ai_usecase import LoadTaskOpenAiUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, TermsNotAccepted
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created


class LoadTaskOpenAiController:
    def __init__(self, usecase: LoadTaskOpenAiUsecase) -> None:
        self.loadTaskOpenAiUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('task_message') is None:
                raise MissingParameters('task_message')

            task_message = request.data.get('task_message')
            response = self.loadTaskOpenAiUsecase(task_message)

            viewmodel = LoadTaskOpenAiViewodel(response)
            return Created(body=viewmodel.to_dict())

        except DuplicatedItem as err:
            return Conflict(body=f"Usuário já cadastrado com esses dados: {err.message}" if err.message != "user" else "Usuário já cadastrado com esses dados")

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
