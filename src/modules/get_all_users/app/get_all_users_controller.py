from .get_all_users_usecase import GetAllUsersUsecase
from .get_all_users_viewmodel import GetAllUsersViewmodel
from shared.helpers.errors.domain_errors import EntityError
from shared.helpers.errors.usecase_errors import NoItemsFound
from shared.helpers.external_interfaces.external_interface import IRequest
from shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class GetAllUsersController:
  def __init__(self, usecase: GetAllUsersUsecase):
    self.usecase = usecase
    
  def handle(self, request: IRequest):
    try:
      users = self.usecase.execute()
      
      viewmodel = GetAllUsersViewmodel(users)
      
      return OK(viewmodel.to_dict())
    
    except NoItemsFound as e:
      return NotFound(str(e))
    except EntityError as e:
      return BadRequest(str(e))
    except Exception as e:
      return InternalServerError(str(e))
    
      