from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .update_task_controller import UpdateTaskController
from .update_task_usecase import UpdateTaskUsecase

repo = Environments.get_task_repo()
usecase = UpdateTaskUsecase(repo)
controller = UpdateTaskController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.to_dict()