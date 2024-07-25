from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .create_category_controller import CreateCategoryController
from .create_category_usecase import CreateCategoryUsecase

repo = Environments.get_category_repo()
usecase = CreateCategoryUsecase(repo)
controller = CreateCategoryController(usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(event)
    httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.to_dict()
