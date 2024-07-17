from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_task_by_id_controller import GetTaskByIdController
from .get_task_by_id_usecase import GetTaskByIdUsecase

repo = Environments.get_task_repo()
usecase = GetTaskByIdUsecase(repo)
controller = GetTaskByIdController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.to_dict()