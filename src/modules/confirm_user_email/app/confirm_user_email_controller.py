from src.shared.helpers.errors.domain_errors import EntityError
from .confirm_user_email_usecase import ConfirmUserEmailUsecase
from .confirm_user_email_viewmodel import ConfirmUserEmailViewmodel
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class ConfirmUserEmailController:
  def __init__(self, usecase: ConfirmUserEmailUsecase) -> None:
    self.usecase = usecase
    
  def __call__(self, request: IRequest):
    try:
      if request.data.get('email') is None:
        raise MissingParameters('email')
      if request.data.get('verification_code') is None:
        raise MissingParameters('verification_code')
      
      if type(request.data.get('email')) is not str:
        raise WrongTypeParameter('email', 'string', type(request.data.get('email')))
      if type(request.data.get('verification_code')) is not str:
        raise WrongTypeParameter('verification_code', 'string', type(request.data.get('verification_code')))
      
      self.usecase(request.data.get('email'), request.data.get('verification_code'))
      
      viewmodel = ConfirmUserEmailViewmodel()
      
      return OK(viewmodel.to_dict())
    
    except MissingParameters as e:
      return BadRequest(body=e.message)
    except WrongTypeParameter as e:
      return BadRequest(body=e.message)
    except NoItemsFound as e:
      return BadRequest(body=e.message)
    except EntityError as e:
      return BadRequest(body=e.message)
    except Exception as e:
      return InternalServerError(body=f"Internal server error: {str(e)}")
      
       
      