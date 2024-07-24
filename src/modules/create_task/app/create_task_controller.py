from src.shared.domain.entities.task import Task
from src.shared.environments import Environments, STAGE
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO
from .create_task_usecase import CreateTaskUsecase
from .create_task_viewmodel import CreateTaskViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, InvalidCredentials, TermsNotAccepted
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, Created


class CreateTaskController:
    def __init__(self, usecase: CreateTaskUsecase) -> None:
        self.createTaskUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            print(f"request.data.get('requester_user'): {request.data.get('requester_user')}")
            
            if request.data.get('task_name') is None:
                raise MissingParameters('task_name')
            if request.data.get('task_date') is None:
                raise MissingParameters('task_date')
            if request.data.get('task_hour') is None:
                raise MissingParameters('task_hour')
            if request.data.get('task_status') is None:
                raise MissingParameters('task_status')

            
            if request.data.get('task_description') is None:
                print("FUNFOU CACETE")
                task_description = None
            else:
                print("PROVAVELMENTE DEU MERDA!!!!!!!!!!!!")
                task_description = request.data.get('task_description')
                
            if request.data.get('task_local') is None:
                print('funfou pra caralho!')
                task_local = None
            else:
                print("deu merda..")
                task_local = request.data.get('task_local')
            
            if Environments.get_envs().stage is not STAGE.TEST:
                if request.data.get('requester_user') is None:
                    raise MissingParameters('requester_user')
                user_id = UserAPIGatewayDTO.from_api_gateway(request.data.get('requester_user')).to_dict().get('user_id')
            
            
            task_dict = {
                'task_name': request.data.get('task_name'),
                'user_id': user_id,
                'task_date': request.data.get('task_date'),
                'task_hour': request.data.get('task_hour'),
                'task_description': task_description,
                'task_local': task_local,
                'task_status': request.data.get('task_status')
            }

            new_task = Task.parse_object(task_dict)
            create_task = self.createTaskUsecase(new_task)

            viewmodel = CreateTaskViewmodel(create_task)
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
