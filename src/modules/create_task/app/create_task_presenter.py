from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .create_task_usecase import CreateTaskUsecase
from .create_task_controller import CreateTaskController

repo = Environments.get_task_repo()()
usecase = CreateTaskUsecase(repo)
controller = CreateTaskController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    response = controller.handle(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
