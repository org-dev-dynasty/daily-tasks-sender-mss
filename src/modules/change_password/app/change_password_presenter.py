from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .change_password_controller import ChangePasswordController
from .change_password_usecase import ChangePasswordUsecase

repo = Environments.get_user_repo()
usecase = ChangePasswordUsecase(repo)
controller = ChangePasswordController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller.handle(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
