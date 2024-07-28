from src.shared.domain.enums.stage_enum import STAGE
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError
from .change_password_usecase import ChangePasswordUsecase
from .change_password_viewmodel import ChangePasswordViewmodel
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter

class ChangePasswordController:
    def __init__(self, usecase: ChangePasswordUsecase):
        self.usecase = usecase
    
    def handle(self, request: IRequest):
        try:
            if Environments.get_envs().stage is not STAGE.TEST:
                if request.data.get('requester_user') is None:
                    raise MissingParameters('requester_user')
            
            if request.data.get('oldPassword') is None:
                raise MissingParameters('oldPassword')
            if type(request.data.get('oldPassword')) is not str:
                raise WrongTypeParameter('oldPassword', 'string', type(request.data.get('oldPassword')))
            if request.data.get('newPassword') is None:
                raise MissingParameters('newPassword')
            if type(request.data.get('newPassword')) is not str:
                raise WrongTypeParameter('newPassword', 'string', type(request.data.get('newPassword')))
            if request.data.get('access_token') is None:
                raise MissingParameters('access_token')
            if type(request.data.get('access_token')) is not str:
                raise WrongTypeParameter('access_token', 'string', type(request.data.get('access_token')))
            
            response = self.usecase.execute(
                request.data.get('oldPassword'), 
                request.data.get('newPassword'), 
                request.data.get('access_token')
            )
            viewmodel = ChangePasswordViewmodel(response)

            return OK(viewmodel.to_dict())

        except MissingParameters as e:
            raise BadRequest(body=e.message)
        except WrongTypeParameter as e:
            raise BadRequest(body=e.message)
        except EntityError as e:
            raise BadRequest(body=e.message)
        except Exception as e:
            raise InternalServerError(body=f"Internal server error: {str(e)}")