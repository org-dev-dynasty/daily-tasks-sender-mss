from .get_all_users_usecase import GetAllUsersUsecase
from .get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class GetAllUsersController:

  def __init__(self, usecase: GetAllUsersUsecase):
    self.usecase = usecase
    

  def handle(self, request: IRequest):
    try:
      users = self.usecase.execute()
      
      print(f'usecase resp controller: {users}')
      
      viewmodel = GetAllUsersViewmodel(users)
      
      print(f'viewmodel: {viewmodel.to_dict()}')
      
      
      return OK(viewmodel.to_dict())
    
    except NoItemsFound as e:
      return NotFound(str(e))
    except EntityError as e:
      return BadRequest(str(e))
    except Exception as e:
      return InternalServerError(str(e))
    