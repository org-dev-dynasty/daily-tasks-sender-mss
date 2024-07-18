from src.shared.environments import Environments
from .update_task_status_usecase import UpdateTaskStatusUsecase
from .update_task_status_controller import UpdateTaskStatusController
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_task_repo()
usecase = UpdateTaskStatusUsecase(repo)
controller = UpdateTaskStatusController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.to_dict()
