from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .delete_account_controller import DeleteAccountController
from .delete_account_usecase import DeleteAccountUsecase

repo = Environments.get_user_repo()
usecase = DeleteAccountUsecase(repo)
controller = DeleteAccountController(usecase)

def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = controller(httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  return httpResponse.to_dict()
