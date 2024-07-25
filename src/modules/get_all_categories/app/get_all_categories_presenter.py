

from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_all_categories_controller import GetAllCategoriesController
from .get_all_categories_usecase import GetAllCategoriesUsecase
from src.shared.environments import Environments


repo = Environments.get_category_repo()
usecase = GetAllCategoriesUsecase(repo)
controller = GetAllCategoriesController(usecase)

def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = controller(httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  return httpResponse.to_dict()