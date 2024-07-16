from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .login_usecase import LoginUseCase
from .login_controller import LoginController

repo = Environments.get_user_repo()
usecase = LoginUseCase(repo)
controller = LoginController(usecase)


def login_user_presenter(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return http_response.to_dict()


def lambda_handler(event, context):
    response = login_user_presenter(event, context)
    return response