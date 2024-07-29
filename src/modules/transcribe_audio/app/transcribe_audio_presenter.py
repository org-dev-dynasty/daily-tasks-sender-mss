from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .transcribe_audio_controller import TranscribeAudioController
from .transcribe_audio_usecase import TranscribeAudioUsecase

repo = Environments.get_task_repo()
usecase = TranscribeAudioUsecase(repo)
controller = TranscribeAudioController(usecase)

def lambda_handler(event, context):
  httpRequest = LambdaHttpRequest(event)
  # httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = controller(httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  return httpResponse.to_dict()
