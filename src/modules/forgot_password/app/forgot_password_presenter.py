from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.modules.forgot_password.app.forgot_password_controller import ForgotPasswordController
from src.modules.forgot_password.app.forgot_password_usecase import ForgotPasswordUsecase


repo = Environments.get_user_repo()
usecase = ForgotPasswordUsecase(repo)
controller = ForgotPasswordController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
