import logging
print("ENTRANDO NO PRESENTER")
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .create_user_usecase import CreateUserUsecase
from .create_user_controller import CreateUserController

print("IMPORTOU TUDO e entrando no REPO DE USER")
repo = Environments.get_user_repo()()
print("REPO DE USER INSTANCIADO")
logging.info(repo)
print("CHAMANDO O USECASE DE CREATE USER")
usecase = CreateUserUsecase(repo)
print('USECASE DE CREATE USER INSTANCIADO')
logging.info(usecase)
print("CHAMANDO O CONTROLLER DE CREATE USER")
controller = CreateUserController(usecase)
print("CONTROLLER DE CREATE USER INSTANCIADO")
logging.info(controller)


def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  print(f'httpRequest: {httpRequest}')
  response = controller.handle(httpRequest)
  print(f'response: {response}')
  print(f'response.body: {response.body}')
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  print(f'httpResponse: {httpResponse}')
  return httpResponse.to_dict()