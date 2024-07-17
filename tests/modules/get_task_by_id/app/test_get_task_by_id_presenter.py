import json
import pytest

from src.modules.get_task_by_id.app.get_task_by_id_presenter import lambda_handler
from src.shared.infra.repositories.task_repository_mock import TaskRepositoryMock


class Test_GetTaskByIdPresenter:
    repo_mock = TaskRepositoryMock()

    def test_get_task_by_id_presenter(self):

        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "task_id=1",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "task_id": "1",
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
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "http": {
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
            "body": json.dumps({
                "task_name": "TaskUm",
                "task_date": "2021-12-12",
                "task_hour": "12:00:00",
                "task_description": "Description for task 1",
                "task_local": "Local 1",
                "task_status": "ACTIVE"
            }),
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        expected = {
            "task_id": "1",
            "task_name": 'TaskUm',
            "task_date": "2021-12-12",
            "task_hour": "12:00:00",
            "task_description": "Description for task 1",
            "task_local": "Local 1",
            "task_status": "ACTIVE"
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "the task was retrieved"
        assert json.loads(response["body"])["task"] == expected
