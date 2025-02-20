from .delete_task_by_id_usecase import DeleteTaskByIdUsecase
from .delete_task_by_id_viewmodel import DeleteTaskByIdViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError


class DeleteTaskByIdController:

    def __init__(self, usecase: DeleteTaskByIdUsecase):
        self.DeleteTaskByIdUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get("task_id") is None:
                raise MissingParameters("task_id")

            self.DeleteTaskByIdUsecase(task_id=request.data.get(
                "task_id"))

            viewmodel = DeleteTaskByIdViewmodel()

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except NotFound as err:

            return NotFound(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
