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
            if Environments.get_envs().stage.value is not STAGE.TEST.value:
                print("entrou no if PRA PEGAR O REQUESTER USER")
                print(request.data.get('requester_user'))
                if request.data.get('requester_user') is None:
                    raise MissingParameters('requester_user')
                print(request.data.get('requester_user'))
            
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

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:
            return InternalServerError(body=err.args[0])
