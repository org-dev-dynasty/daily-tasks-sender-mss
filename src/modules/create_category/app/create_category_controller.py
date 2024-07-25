from .create_category_usecase import CreateCategoryUsecase
from .create_category_viewmodel import CreateCategoryViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Created
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidCredentials
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO
from src.shared.environments import Environments, STAGE
from src.shared.domain.entities.category import Category

class CreateCategoryController:
    def __init__(self, usecase: CreateCategoryUsecase):
        self.usecase = usecase
    
    def __call__(self, request: IRequest):
        try:
            if Environments.get_envs().stage is not STAGE.TEST:
                if request.data.get('requester_user') is None:
                    raise MissingParameters('requester_user')
                user_id = UserAPIGatewayDTO.from_api_gateway(request.data.get('requester_user')).to_dict().get('user_id')

            if request.data.get("category_primary_color") is None:
                raise MissingParameters("category_primary_color")
            if request.data.get("category_secondary_color") is None:
                raise MissingParameters("category_secondary_color")
            
            category_name = request.data.get("category_name") if request.data.get("category_name") != "" else None

            category_dict = {
                'category_name': category_name,
                'category_primary_color': request.data.get('category_primary_color'),
                'category_secondary_color': request.data.get('category_secondary_color'),
                'user_id': user_id
            }

            new_category = Category.parse_object(category_dict)
            self.usecase.execute(new_category)
            viewmodel = CreateCategoryViewmodel.to_dict()
            
            return Created(viewmodel)

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:
            return InternalServerError(body=err.args[0])
