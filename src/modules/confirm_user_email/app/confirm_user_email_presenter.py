import logging
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .confirm_user_email_usecase import ConfirmUserEmailUsecase
from .confirm_user_email_controller import ConfirmUserEmailController

repo = Environments.get_task_repo()
logging.info(repo)
usecase = ConfirmUserEmailUsecase(repo)
logging.info(usecase)
controller = ConfirmUserEmailController(usecase)
logging.info(controller)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
