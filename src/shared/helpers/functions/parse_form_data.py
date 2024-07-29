from multipart import parse_options_header, MultipartParser
import base64
import io

from src.shared.helpers.external_interfaces.external_interface import IRequest

def formdata_parser(event):
  try:
    content_type = event['headers']['content-type'] if 'content-type' in event['headers'] else event['headers']['Content-Type']

    _, options = parse_options_header(content_type)
    boundary = options['boundary'].encode('utf-8')
    body = base64.b64decode(event["body"]) if event["isBase64Encoded"] else event["body"].encode('utf-8')
    
    body_stream = io.BytesIO(body)
    
    parser = MultipartParser(body_stream, boundary)
    
    return parser
    
  except Exception as e:
    print(f'ERROR PARSING FORM DATA {e}')
    raise ValueError("An error occurred while parsing form data")