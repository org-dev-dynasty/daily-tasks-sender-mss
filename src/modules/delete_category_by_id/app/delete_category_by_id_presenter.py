from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .delete_category_by_id_controller import DeleteCategoryByIdController
from .delete_category_by_id_usecase import DeleteCategoryByIdUsecase

repo = Environments.get_category_repo()
usecase = DeleteCategoryByIdUsecase(repo)
controller = DeleteCategoryByIdController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.to_dict()
