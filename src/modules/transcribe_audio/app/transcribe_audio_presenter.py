from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.functions.parse_form_data import formdata_parser
from src.shared.infra.repositories.audio_repository_openai import AudioRepositoryOpenAI
from .transcribe_audio_controller import TranscribeAudioController
from .transcribe_audio_usecase import TranscribeAudioUsecase

repo = AudioRepositoryOpenAI()
usecase = TranscribeAudioUsecase(repo)
controller = TranscribeAudioController(usecase)

def lambda_handler(event, context):
  print(event)
  parser = formdata_parser(event)
  httpRequest = LambdaHttpRequest(event)
  httpRequest.data['formdata_parser'] = parser
  # httpRequest.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
  response = controller(httpRequest)
  httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
  return httpResponse.to_dict()
