import logging
import os
print(os.getcwd())
print(os.listdir())
print(os.listdir('../../opt/python'))

from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .create_user_oauth_controller import CreateUserOAuthController
from .create_user_oauth_controller import CreateUserOAuthUsecase

repo = Environments.get_user_repo()
logging.info(repo)
usecase = CreateUserOAuthUsecase(repo)
logging.info(usecase)
controller = CreateUserOAuthController(usecase)
logging.info(controller)


def lambda_handler(event, context):
  print(f'event: {event}')
  httpRequest = LambdaHttpRequest(event)
  print(f'httpRequest: {httpRequest}')
  response = controller(httpRequest)
  print(f'response: {response}')
  print(f'response.body: {response.body}')
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  print(f'httpResponse: {httpResponse}')
  return httpResponse.to_dict()