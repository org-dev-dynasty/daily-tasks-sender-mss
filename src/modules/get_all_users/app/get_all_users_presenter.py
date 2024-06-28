import logging
import os

from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_all_users_usecase import GetAllUsersUsecase
from .get_all_users_controller import GetAllUsersController

repo = Environments.get_user_repo()()
logging.info(repo)
usecase = GetAllUsersUsecase(repo)
logging.info(usecase)
controller = GetAllUsersController(usecase)
logging.info(controller)


def lambda_handler(event, context):
  print('lambda_handler OOOOIIIII')
  print(f'event: {event}')
  httpRequest = LambdaHttpRequest(event)
  print(f'httpRequest: {httpRequest}')
  response = controller.handle(httpRequest)
  print(f'response: {response}')
  print(f'response.body: {response.body}')
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  print(f'httpResponse: {httpResponse}')
  return httpResponse.to_dict()