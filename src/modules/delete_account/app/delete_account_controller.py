from src.shared.domain.enums.stage_enum import STAGE
from src.shared.environments import Environments
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, NotFound
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO
from .delete_account_viewmodel import DeleteAccountViewmodel
from .delete_account_usecase import DeleteAccountUsecase


class DeleteAccountController:
  def __init__(self, usecase: DeleteAccountUsecase):
    self.usecase = usecase
    
  def __call__(self, request: IRequest):
    user_id = ''
    try:
      if Environments.get_envs().stage is not STAGE.TEST:
                if request.data.get('requester_user') is None:
                    raise MissingParameters('requester_user')
                user_id = UserAPIGatewayDTO.from_api_gateway(request.data.get('requester_user')).to_dict().get('user_id')
                
      self.usecase(user_id)
      
      viewmodel = DeleteAccountViewmodel()
      
      return OK(viewmodel.to_dict())
    
    except NoItemsFound as e:
      return NotFound(e.message)
    except Exception as e:
      return InternalServerError('Internal Server Error: ' + str(e))