from multipart import parse_options_header

from src.shared.helpers.external_interfaces.external_interface import IRequest

def formdata_parser(request: IRequest):
  try:
    content_type = request.data.get('content-type') or request.data.get('Content-Type')
    print('CONTENT TYPE: ')
    print(content_type)
    
    _, options = parse_options_header(content_type)
    boundary = options['boundary'].encode('utf-8')
  except Exception as e:
    print(f'ERROR PARSING FORM DATA {e}')
    raise ValueError("An error occurred while parsing form data")