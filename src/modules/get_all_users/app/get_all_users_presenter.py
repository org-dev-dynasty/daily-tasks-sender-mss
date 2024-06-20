import os 
print(os.listdir(f"./"))
print(os.listdir(f"../"))
print(os.listdir(f"../../"))


from shared.environments import Environments
from shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_all_users_usecase import GetAllUsersUsecase
from .get_all_users_controller import GetAllUsersController

repo = Environments.get_user_repository()
usecase = GetAllUsersUsecase(repo)
controller = GetAllUsersController(usecase)


def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  response = controller.handle(httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  print(f'httpResponse: {httpResponse}')
  return httpResponse.to_dict()