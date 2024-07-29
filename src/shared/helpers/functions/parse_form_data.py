from multipart import parse_options_header, MultipartParser
import base64

from src.shared.helpers.external_interfaces.external_interface import IRequest

def formdata_parser(request: IRequest):
  try:
    content_type = request.data.get('content-type') or request.data.get('Content-Type')
    
    
    _, options = parse_options_header(content_type)
    boundary = options['boundary'].encode('utf-8')
    body = base64.b64decode(request.data.get('body')) if request.data.get("isBase64Encoded") else request.data.get('body').encode('utf-8')
    
    parser = MultipartParser(body, boundary)
    
    return parser
    
  except Exception as e:
    print(f'ERROR PARSING FORM DATA {e}')
    raise ValueError("An error occurred while parsing form data")