from src.shared.environments import Environments
from .get_task_by_day_controller import GetTaskByDayController
from .get_task_by_day_usecase import GetTaskByDayUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_task_repo()
usecase = GetTaskByDayUsecase(repo)
controller = GetTaskByDayController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
