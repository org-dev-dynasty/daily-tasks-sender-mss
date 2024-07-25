from .refresh_token_usecase import RefreshTokenUsecase
from .refresh_token_viewmodel import RefreshTokenViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidTokenError
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class RefreshTokenController:
  def __init__(self, usecase: RefreshTokenUsecase):
    self.usecase = usecase
    
  def __call__(self, request: IRequest):
    try:
      if request.data.get('Authorization') is None:
        raise MissingParameters('Authorization')
      
      split_token = request.data.get('Authorization').split(' ')
      if len(split_token) != 2:
        raise MissingParameters('Authorization')
      if split_token[0] != 'Bearer':
        raise MissingParameters('Authorization')
      
      refresh_token = split_token[1]
      
      access_token, id_token, refresh_token = self.usecase(refresh_token)
      
      viewmodel = RefreshTokenViewmodel(access_token, id_token, refresh_token)
      
      return OK(viewmodel.to_dict())
    
    except MissingParameters as err:
      return BadRequest(body=err.message)
    except ForbiddenAction as err:
      return BadRequest(body=err.message)
    except InvalidTokenError as err:
      return BadRequest(body="Token inválido, por favor faça login novamente")
    except Exception as err:
      return InternalServerError(body=err.args[0])
    
    