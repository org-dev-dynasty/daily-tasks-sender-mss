from typing import Tuple
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class RefreshTokenUsecase:
  def __init__(self, repo: IUserRepository):
    self.repo = repo
  
  def __call__(self, refresh_token: str) -> Tuple[str, str]:
    tokens = self.repo.refresh_token(refresh_token)
    if tokens is None or tokens == (None, None):
      raise ForbiddenAction(f'Refresh Token: {refresh_token}')
    
    access_token, id_token, refresh_token = tokens
    
    if access_token is None or id_token is None or refresh_token is None:
      raise ForbiddenAction(f'Refresh, access or id token: {refresh_token}, {access_token}, {id_token}')
    
    return access_token, id_token, refresh_token
    