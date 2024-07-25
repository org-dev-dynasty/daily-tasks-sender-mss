from src.shared.domain.enums.stage_enum import STAGE
from src.shared.environments import Environments
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO
from .get_all_categories_viewmodel import GetAllCategoriesViewmodel
from .get_all_categories_usecase import GetAllCategoriesUsecase


class GetAllCategoriesController:
  def __init__(self, usecase: GetAllCategoriesUsecase):
    self.usecase = usecase
    
  def __call__(self, request: IRequest):
    try:
      if Environments.get_envs().stage is not STAGE.TEST:
        if request.data.get('requester_user') is None:
          raise MissingParameters('requester_user')
        user_id = UserAPIGatewayDTO.from_api_gateway(request.data.get('requester_user')).to_dict().get('user_id')
        
      categories = self.usecase.execute(user_id)
      print("categories")
      print(categories)
      viewmodel = GetAllCategoriesViewmodel(categories) 
      
      return OK(viewmodel.to_dict())
    
    except MissingParameters as err:
      return BadRequest(body=err.message)
    except Exception as err:
      return InternalServerError(body=err.args[0])
    
      
        
        