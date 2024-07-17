from .get_all_tasks_usecase import GetAllTasksUsecase
from .get_all_tasks_viewmodel import GetAllTasksViewmodel
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, NotFound, InternalServerError

class GetAllTasksController:

    def __init__(self, usecase: GetAllTasksUsecase):
        self.usecase = usecase

    def handle(self, request: IRequest):
        try:

            users = self.usecase.execute()
            viewmodel = GetAllTasksViewmodel(users)

            return OK(viewmodel.to_dict())
        except NoItemsFound as e:
            return NotFound(str(e))
        except EntityError as e:
            return BadRequest(str(e))
        except Exception as e:
            return InternalServerError(str(e))
