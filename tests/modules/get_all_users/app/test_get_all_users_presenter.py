import json

from src.modules.get_all_users.app.get_all_users_presenter import lambda_handler


class Test_GetAllUsersPresenter:
    # FIXME: Erro relacionado ao UserRepositoryPostgres
    def test_get_all_users_presenter(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "value1",
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user_id/example-user_id",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": "Hello from client!",
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        expected_body = {
            "users": [
                {
                    'name': "Digao",
                    'email': "digao@gmail.com",
                    'phone': '11999999999',
                    'password': 'Teste12@'
                },
                {
                    'name': "Ale",
                    'email': "ale@gmail.com",
                    'phone': '11299999999',
                    'password': 'Teste1@'
                },
                {
                    'name': "Lucao",
                    'email': "lucao@gmail.com",
                    'phone': '11399999999',
                    'password': 'Teste13@'
                },
                {
                    'name': "Brenheta",
                    'email': "brenheta@gmail.com",
                    'phone': '11499999999',
                    'password': 'Teste14@'
                },
                {
                    'name': "Merola",
                    'email': "merola.gay@gmail.com",
                    'phone': '11599999999',
                    'password': 'Teste15@'
                }
            ],
            "message": "All users have been retrieved successfully!"
        }

        response = lambda_handler(event=event, context=None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == expected_body
