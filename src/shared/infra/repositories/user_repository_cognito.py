from typing import List, Dict
import boto3
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, UserAlreadyConfirmed, NoItemsFound, \
    InvalidCredentials, UserNotConfirmed, DuplicatedItem, InvalidTokenError
from src.shared.infra.dto.user_cognito_dto import UserCognitoDTO


class UserRepositoryCognito(IUserRepository):
    client: boto3.client
    user_pool_id: str
    client_id: str

    def __init__(self):
        self.client = boto3.client('cognito-idp')
        self.user_pool_id = Environments.get_envs().user_pool_id
        self.client_id = Environments.get_envs().client_id

    def login_user(self, email: str, password: str) -> Dict:
        try:
            response_login = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            access_token = response_login["AuthenticationResult"]["AccessToken"]
            response_get_user = self.client.get_user(
                AccessToken=access_token
            )

            user = UserCognitoDTO.from_cognito(response_get_user).to_entity()

            dict_response = user.to_dict()
            dict_response["access_token"] = response_login["AuthenticationResult"]["AccessToken"]
            dict_response["refresh_token"] = response_login["AuthenticationResult"]["RefreshToken"]
            dict_response["id_token"] = response_login["AuthenticationResult"]["IdToken"]
            return dict_response

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['NotAuthorizedException', 'UserNotFoundException']:
                raise InvalidCredentials("Invalid email or password")
            elif error_code == 'UserNotConfirmedException':
                raise UserNotConfirmed("User not confirmed")
            else:
                raise EntityError("An error occurred during login")

    def get_all_users(self) -> List[Dict]:
        users = []
        try:
            response = self.client.list_users(
                UserPoolId=self.user_pool_id
            )
            while True:
                for user in response.get('Users', []):
                    user_dto = UserCognitoDTO.from_cognito(user)
                    user_dict = user_dto.to_dict()
                    users.append(user_dict)

                if 'PaginationToken' not in response:
                    break

                response = self.client.list_users(
                    UserPoolId=self.user_pool_id,
                    PaginationToken=response['PaginationToken']
                )

        except ClientError as e:
            raise EntityError("An error occurred while fetching users")

        return users
