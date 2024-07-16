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

    def login(self, email: str, password: str) -> Dict:
        try:
            print(f'USER REPO COGNITO - client_id {self.client_id}')
            print(f'USER REPO COGNITO - user_pool_id {self.user_pool_id}')
            base_pwd_cognito = Environments.get_envs().base_pwd_cognito
            response_login = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': base_pwd_cognito
                }
            )
            
            dict_response = {
                'access_token': response_login['AuthenticationResult']['AccessToken'],
                'id_token': response_login['AuthenticationResult']['IdToken'],
                'refresh_token': response_login['AuthenticationResult']['RefreshToken']
            }
            
            return dict_response

        except ClientError as e:
            error_code = e.response['Error']['Code']
            print(f'e.response {e.response}')
            print(f'error_code {error_code}')
            if error_code in ['NotAuthorizedException', 'UserNotFoundException']:
                raise InvalidCredentials("Invalid email or password")
            elif error_code == 'UserNotConfirmedException':
                raise UserNotConfirmed("User not confirmed")
            elif error_code == 'UserNotFoundException' or error_code == 'ResourceNotFoundException':
                raise NoItemsFound("user")
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

    def create_user(self, user: User) -> User:
        cognito_attributes = UserCognitoDTO.from_entity(
            user).to_cognito_attributes()
        cognito_attributes.pop("password")
        cognito_attributes.pop("email")
        try:

            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=user.email,
                Password=user.password,
                UserAttributes=cognito_attributes)
            
            print(f'USER REPO COGNITO response CREATE USER {response}')

            user.cognito_id = response.get("UserSub")
            
            base_pwd_cognito = Environments.get_envs().base_pwd_cognito
            response_login = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': user.email,
                    'PASSWORD': base_pwd_cognito
                }
            )
            
            print(f'USER REPO COGNITO response INITIATE AUTH CREATE USER {response_login}')
            
            if 'ChallengeName' in response_login and response_login['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
                session = response_login['Session']
                self.client.respond_to_auth_challenge(
                    ClientId=self.client_id,
                    ChallengeName='NEW_PASSWORD_REQUIRED',
                    Session=session,
                    ChallengeResponses={
                        'USERNAME': user.email,
                        'NEW_PASSWORD': user.password
                    }
                )
            
            return user

        except self.client.exceptions.UsernameExistsException:
            raise DuplicatedItem("email")

        except self.client.exceptions.InvalidPasswordException:
            raise InvalidCredentials("password")

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
