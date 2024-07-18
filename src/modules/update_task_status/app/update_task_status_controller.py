from .update_task_status_usecase import UpdateTaskStatusUsecase
from .update_task_status_viewmodel import UpdateTaskStatusViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK
from src.shared.helpers.errors.usecase_errors import InvalidCredentials
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError

class UpdateTaskStatusController:
    def __init__(self, usecase: UpdateTaskStatusUsecase):
        self.usecase = usecase
    
    def __call__(self, request: IRequest):
        try:
            if not request.data.get("task_id"):
                return MissingParameters("Task id is required")
            if not request.data.get("task_status"):
                return MissingParameters("Task status is required")
            
            task_id = request.data.get("task_id")
            task_status = request.data.get("task_status")
            
            task = self.usecase.execute(task_id, task_status)
            viewmodel = UpdateTaskStatusViewmodel()

            return OK(viewmodel.to_dict())
        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:
            return InternalServerError(body=err.args[0])
