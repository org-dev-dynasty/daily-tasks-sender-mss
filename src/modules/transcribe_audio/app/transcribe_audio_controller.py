from src.modules.transcribe_audio.app.transcribe_audio_usecase import TranscribeAudioUsecase
from src.shared.domain.enums.stage_enum import STAGE
from src.shared.environments import Environments
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError
from src.shared.helpers.functions.parse_form_data import formdata_parser
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO


class TranscribeAudioController:
  def __init__(self, usecase: TranscribeAudioUsecase):
    self.usecase = usecase
    
  def __call__(self, request: IRequest):
    try:
      # if Environments.get_envs().stage is not STAGE.TEST:
      #   if request.data.get('requester_user') is None:
      #       raise MissingParameters('requester_user')
      #   user_id = UserAPIGatewayDTO.from_api_gateway(request.data.get('requester_user')).to_dict().get('user_id')
      
      formdata_parsed = formdata_parser(request)
      
      
      return OK('Transcription successful')
    
    except Exception as e:
      return InternalServerError('Internal Server Error: ' + str(e))
    