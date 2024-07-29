from src.shared.domain.enums.stage_enum import STAGE
from src.shared.environments import Environments
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError
from src.shared.helpers.functions.parse_form_data import formdata_parser
from src.shared.infra.dto.user_api_gateway_dto import UserAPIGatewayDTO
from .transcribe_audio_usecase import TranscribeAudioUsecase


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
      
      audio_file = None
      
      for part in formdata_parsed:
        if part.name == 'file':
          audio_file = part
          
        
      if audio_file is None:
        raise MissingParameters('audio_file')
      
      
      return OK('Transcription successful')
    
    except MissingParameters as e:
      return BadRequest(e.message)
    
    except Exception as e:
      return InternalServerError('Internal Server Error: ' + str(e))
    