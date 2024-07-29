from src.modules.get_all_inactives_tasks.app.get_all_inactives_tasks_usecase import GetAllInactivesTasksUsecase
from src.modules.get_all_inactives_tasks.app.get_all_inactives_tasks_viewmodel import GetAllInactivesTasksViewmodel
from src.shared.domain.enums.stage_enum import STAGE
from src.shared.environments import Environments
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO


class GetAllInactivesTasksController:
    def __init__(self, usecase: GetAllInactivesTasksUsecase):
        self.usecase = usecase
    
    def handle(self, request: IRequest):
        try:
            if Environments.get_envs().stage is not STAGE.TEST:
                if request.data.get('requester_user') is None:
                    raise MissingParameters('requester_user')
                user_id = UserAPIGatewayDTO.from_api_gateway(request.data.get('requester_user')).to_dict().get('user_id')
            
            tasks = self.usecase.execute(user_id=user_id)
            viewmodel = GetAllInactivesTasksViewmodel('Tasks encontradas com sucesso!')

            return OK(viewmodel.to_dict(tasks=tasks))
            # return OK(tasks)
        except NoItemsFound as e:
            return NotFound(str(e))
        except EntityError as e:
            return BadRequest(str(e))
        except Exception as e:
            return InternalServerError(str(e))
