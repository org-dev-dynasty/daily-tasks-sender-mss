from .update_task_usecase import UpdateTaskUsecase
from .update_task_viewmodel import UpdateTaskViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, OK

class UpdateTaskController:
    def __init__(self, usecase: UpdateTaskUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            if request.data.get("task_id") is None:
                raise MissingParameters("task_id")
            
            updateTask = {}

            if request.data.get("task_name") is not None:
                updateTask["task_name"] = request.data.get("task_name")
            if request.data.get("task_date") is not None:
                updateTask["task_date"] = request.data.get("task_date")
            if request.data.get("task_hour") is not None:
                updateTask["task_hour"] = request.data.get("task_hour")
            if request.data.get("task_description") is not None:
                updateTask["task_description"] = request.data.get("task_description")
            if request.data.get("task_local") is not None:
                updateTask["task_local"] = request.data.get("task_local")
            if request.data.get("task_status") is not None:
                updateTask["task_status"] = request.data.get("task_status")
            if request.data.get("category_id") is not None:
                updateTask["category_id"] = request.data.get("category_id")
            
            self.usecase.execute(
                task_id=request.data.get("task_id"),
                category_id=updateTask.get("category_id"),
                task_name=updateTask.get("task_name"),
                task_date=updateTask.get("task_date"),
                task_hour=updateTask.get("task_hour"),
                task_description=updateTask.get("task_description"),
                task_local=updateTask.get("task_local"),
                task_status=updateTask.get("task_status"),
            )

            viewmodel = UpdateTaskViewmodel()

            return OK(body=viewmodel.to_dict())
        except Exception as err:
            return InternalServerError(body=err.args[0])