from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError
from .forgot_password_usecase import ForgotPasswordUsecase
from .forgot_password_viewmodel import ForgotPasswordViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest


class ForgotPasswordController:
  def __init__(self, usecase: ForgotPasswordUsecase) -> None:
    self.usecase = usecase
    
  def __call__(self, request: IRequest):
    try:
      if request.data.get('email') is None:
        raise MissingParameters('email')
      if type(request.data.get('email')) is not str:
        raise WrongTypeParameter('email', 'str', type(request.data.get('email')))
      
      self.usecase(email=request.data.get('email'))
      
      viewmodel = ForgotPasswordViewmodel()
      
      return OK(body=viewmodel.to_dict())
    
    except EntityError as err:
      return BadRequest(body=err.message)
    except NoItemsFound as err:
      return BadRequest(body=err.message)
    except MissingParameters as err:
      return BadRequest(body=err.message)
    except WrongTypeParameter as err:
      return BadRequest(body=err.message)
    except Exception as err:
      return InternalServerError(body=f"Internal Server Error: {err.args[0]}")
      