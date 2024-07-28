import boto3
from typing import List, Dict, Tuple
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError, WrongEntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, InvalidCredentials, UserNotConfirmed, DuplicatedItem, InvalidTokenError
from src.shared.infra.dto.user_cognito_dto import UserCognitoDTO
from src.shared.infra.services import generate_confirmation_code
from src.shared.infra.services.generate_random_password import generate_random_password
from src.shared.infra.services.send_mail import send_confirmation_code_mail, send_forgot_pwd_mail


class UserRepositoryCognito(IUserRepository):
    client: boto3.client
    user_pool_id: str
    client_id: str

    def __init__(self):
        self.client = boto3.client('cognito-idp')
        self.user_pool_id = Environments.get_envs().user_pool_id
        self.client_id = Environments.get_envs().client_id
    
    def get_user_by_email(self, email: str) -> User:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            return UserCognitoDTO.from_cognito(response).to_entity()
        except ClientError as e:
            raise ValueError("An error occurred while getting user by email: " + str(e))

    def login(self, email: str, password: str) -> Dict:
        try:
            print(f'USER REPO COGNITO - client_id {self.client_id}')
            print(f'USER REPO COGNITO - user_pool_id {self.user_pool_id}')
            response_login = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
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

    def create_user(self, user: User) -> User:
        cognito_attributes = UserCognitoDTO.from_entity(
            user).to_cognito_attributes()
        print(f"PASSOU PELO TO COGNITO ATTRIBUTES {cognito_attributes}")
        cognito_attributes = [attr for attr in cognito_attributes if attr['Name'] != 'password']
        code = generate_confirmation_code()
        cognito_attributes.append({'Name': 'custom:confirmationCode', 'Value': code})
        try:            
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=user.email,
                Password=user.password,
                UserAttributes=cognito_attributes)
            
            print(f'USER REPO COGNITO response CREATE USER {response}')

            user.user_id = response.get("UserSub")
            
            send_confirmation_code_mail(to_email=user.email, code=code)
            
            return {
                "user": user,
                "verification_code": code
            }

        except self.client.exceptions.UsernameExistsException:
            raise DuplicatedItem("email")

        except self.client.exceptions.InvalidPasswordException:
            raise InvalidCredentials("password")

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
        
    
    def confirm_user(self, email: str, confirmation_code: str):
        try:
            resp = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            
            user_attrs = {attr['Name']: attr['Value'] for attr in resp['UserAttributes']}
            
            print(f'USER REPO COGNITO CONFIRM USER {user_attrs}')
            print(f'USER REPO COGNITO CONFIRM USER {user_attrs.get("custom:confirmationCode")}')
            
            if user_attrs.get('custom:confirmationCode') == confirmation_code:
                self.client.admin_update_user_attributes(
                    UserPoolId=self.user_pool_id,
                    Username=email,
                    UserAttributes=[
                        {'Name': 'email_verified', 'Value': 'true'},
                        {'Name': 'custom:confirmationCode', 'Value': ''}
                    ]
                )
                self.client.admin_confirm_sign_up(
                    UserPoolId=self.user_pool_id,
                    Username=email
                )
                
                return { "message": "User confirmed successfully" }
            else:
                raise WrongEntityError("confirmation_code")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UserNotFoundException':
                raise NoItemsFound("user")
            else:
                raise ValueError("An error occurred while confirming user")
            
    def resend_confirmation_code(self, email: str):
        try:
            resp = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            
            user_attrs = {attr['Name']: attr['Value'] for attr in resp['UserAttributes']}
            code = self.generate_confirmation_code()
            
            self.client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=email,
                UserAttributes=[
                    {'Name': 'custom:confirmationCode', 'Value': code}
                ]
            )
            
            
            self.send_confirmation_code_mail(email, user_attrs.get('name'), code)
            
            return { "message": "Confirmation code sent successfully" }
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UserNotFoundException':
                raise NoItemsFound("user")
            else:
                raise ValueError("An error occurred while resending confirmation code")
            
    def finish_sign_up(self, email: str, password: str):
        base_pwd_cognito = Environments.get_envs().base_pwd_cognito
        try:
            response_login = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': base_pwd_cognito
                }
            )
            
            print(f'USER REPO COGNITO response INITIATE AUTH CREATE USER {response_login}')
            
            if 'ChallengeName' in response_login and response_login['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
                session = response_login['Session']
                resp_tokens = self.client.respond_to_auth_challenge(
                    ClientId=self.client_id,
                    ChallengeName='NEW_PASSWORD_REQUIRED',
                    Session=session,
                    ChallengeResponses={
                        'USERNAME': email,
                        'NEW_PASSWORD': password
                    }
                )
                
                tokens = {
                    'access_token': resp_tokens['AuthenticationResult']['AccessToken'],
                    'id_token': resp_tokens['AuthenticationResult']['IdToken'],
                    'refresh_token': resp_tokens['AuthenticationResult']['RefreshToken']
                }
                
                return tokens
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UserNotFoundException':
                raise NoItemsFound("user")
            else:
                raise ValueError("An error occurred while finishing sign up")
            
    def create_user_oauth(self, user: User) -> dict:
        try:
            resp_create = self.create_user(user)
            code = resp_create.get('verification_code')
            self.send_confirmation_code_mail(user.email, user.name, code)
            
            self.confirm_user(user.email, code)
            
            tokens = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': user.email,
                    'PASSWORD': user.password
                }
            )
            
            dict_response = {
                'access_token': tokens['AuthenticationResult']['AccessToken'],
                'id_token': tokens['AuthenticationResult']['IdToken'],
                'refresh_token': tokens['AuthenticationResult']['RefreshToken']
            }
            
            return dict_response
            
        except DuplicatedItem:
            raise DuplicatedItem("user")
        except InvalidCredentials:
            raise InvalidCredentials("password")
        except EntityError as e:
            raise EntityError(e)
        except WrongEntityError as e:
            raise WrongEntityError(e)
        except ValueError as e:
            raise ValueError(e)
        
    def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )
            
            tokens = {
                'access_token': response['AuthenticationResult']['AccessToken'],
                'id_token': response['AuthenticationResult']['IdToken']
            }
            
            return tokens['access_token'], tokens['id_token'], refresh_token

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NotAuthorizedException':
                raise InvalidTokenError("refresh_token")
            else:
                raise ValueError("An error occurred while refreshing token")
            
    def get_all_users(self) -> List[User]:
        try:
            response = self.client.list_users(
                UserPoolId=self.user_pool_id
            )
            print(f'RESPONSE GET ALL USERS {response}')
            return [UserCognitoDTO.from_cognito(user).to_entity() for user in response['Users']]
        except ClientError as e:
            print(f'ERROR GET ALL USERS {e}')
            raise ValueError("An error occurred while getting all users")
        
    def forgot_password(self, email: str) -> dict:
        gen_pwd = generate_random_password()
        
        try:
            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=email,
                Password=gen_pwd,
                Permanent=True
            )
            
            send_forgot_pwd_mail(to_email=email, gen_pwd=gen_pwd)
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UserNotFoundException':
                raise NoItemsFound("user")
            else:
                raise ValueError("An error occurred while sending forgot password mail")
            
    def change_password(self, oldPassword: str, newPassword: str, access_token: str) -> dict:
        try:
            self.client.change_password(
                PreviousPassword=oldPassword,
                ProposedPassword=newPassword,
                AccessToken=access_token
            )

            return { "message": "Senha alterada com sucesso" }
        except ClientError as e:
            raise ValueError("An error occurred while changing password")
    
