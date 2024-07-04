from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError
from .get_user_by_email_usecase import GetUserByEmailUsecase
from .get_user_by_email_viewmodel import GetUserByEmailViewmodel

class GetUserByEmailController:
    def __init__(self, usecase: GetUserByEmailUsecase):
        self.usecase = usecase
    
    def __call__(self, request: IRequest) -> IResponse:
        try:
            email = request.data.get('email')
            if email is None:
                raise MissingParameters('email')

            user = self.usecase(email)
            viewmodel = GetUserByEmailViewmodel(user)
            return viewmodel
        
        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")
        except Exception as err:
            return InternalServerError(body=err.args[0])
