from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .login_usecase import LoginUsecase
from .login_controller import LoginController

repo = Environments.get_user_repository()()
usecase = LoginUsecase(repo)
controller = LoginController(usecase)


def lambda_handler(event, context, email, password):
    httpRequest = LambdaHttpRequest(event)
    response = controller.handle(httpRequest, email, password)
    print(f'response: {response}')
    print(f'response.body: {response.body}')
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    print(f'httpResponse: {httpResponse}')
    return httpResponse.to_dict()
