import logging

from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .refresh_token_usecase import RefreshTokenUsecase
from .refresh_token_controller import RefreshTokenController
from src.shared.environments import Environments


repo = Environments.get_user_repo()
logging.info(repo)
usecase = RefreshTokenUsecase(repo)
logging.info(usecase)
controller = RefreshTokenController(usecase)
logging.info(controller)

def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  response = controller(httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  return httpResponse.to_dict()