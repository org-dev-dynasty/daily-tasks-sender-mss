from datetime import date
from src.shared.domain.entities.task import Task
from .get_task_by_day_usecase import GetTaskByDayUsecase
from .get_task_by_day_viewmodel import GetTaskByDayViewmodel
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, InternalServerError, BadRequest
from src.shared.helpers.external_interfaces.external_interface import IRequest

class GetTaskByDayController:
    def __init__(self, usecase: GetTaskByDayUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if not request.data.get("task_date"):
                return BadRequest("Task date is required")
            
            if not Task.validate_date(request.data.get("task_date")):
                return BadRequest("Invalid date format")
            
            usecase = self.usecase.execute(request.data.get("task_date"))
            viewmodel = GetTaskByDayViewmodel(usecase)

            return OK(viewmodel.to_dict())
        except NoItemsFound as e:
            return NotFound(str(e))
        except EntityError as e:
            return BadRequest(str(e))
        except Exception as e:
            return InternalServerError(str(e))