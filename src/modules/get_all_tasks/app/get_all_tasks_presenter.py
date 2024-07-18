from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_all_tasks_controller import GetAllTasksController
from .get_all_tasks_usecase import GetAllTasksUsecase

repo = Environments.get_task_repo()
usecase = GetAllTasksUsecase(repo)
controller = GetAllTasksController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    response = controller.handle(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
