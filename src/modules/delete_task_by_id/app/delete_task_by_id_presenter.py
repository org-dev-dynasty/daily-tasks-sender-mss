from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .delete_task_by_id_controller import DeleteTaskByIdController
from .delete_task_by_id_usecase import DeleteTaskByIdUsecase

repo = Environments.get_task_repo()
usecase = DeleteTaskByIdUsecase(repo)
controller = DeleteTaskByIdController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.to_dict()
