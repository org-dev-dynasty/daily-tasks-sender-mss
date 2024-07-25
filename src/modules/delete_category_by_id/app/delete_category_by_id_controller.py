from .delete_category_by_id_usecase import DeleteCategoryByIdUsecase
from .delete_category_by_id_usecase import DeleteCategoryByIdViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.errors.domain_errors import EntityError


class DeleteCategoryByIdController:

    def __init__(self, usecase: DeleteCategoryByIdUsecase):
        self.DeleteCategoryByIdUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get("category_id") is None:
                raise MissingParameters("category_id")

            self.DeleteTaskByIdUsecase(category_id=request.data.get(
                "category_id"))

            viewmodel = DeleteCategoryByIdViewmodel()

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
