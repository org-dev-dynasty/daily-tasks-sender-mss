import logging
import os 
print(os.listdir(f"./"))
print(os.listdir(f"../"))
print(os.listdir(f"../../"))


from src.shared.environments import Environments
print('passou o import do env')
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
print('passou o import do http lambda requests')
from .get_all_users_usecase import GetAllUsersUsecase
print('passou o import do usecase')
from .get_all_users_controller import GetAllUsersController
print('passou o import do controller')

repo = Environments.get_user_repository()
logging.info(repo)
usecase = GetAllUsersUsecase(repo)
logging.info(usecase)
controller = GetAllUsersController(usecase)
logging.info(controller)


def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  response = controller.handle(httpRequest)
  print(f'response: {response}')
  print(f'response.body: {response.body}')
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  print(f'httpResponse: {httpResponse}')
  return httpResponse.to_dict()