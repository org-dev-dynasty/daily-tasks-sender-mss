from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_all_inactives_tasks_controller import GetAllInactivesTasksController
from .get_all_inactives_tasks_usecase import GetAllInactivesTasksUsecase

repo = Environments.get_task_repo()
usecase = GetAllInactivesTasksUsecase(repo)
controller = GetAllInactivesTasksController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller.handle(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.to_dict()
