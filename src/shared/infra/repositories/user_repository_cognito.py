import os
import boto3
import random
import string
from typing import List, Dict
from mailersend import emails
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.irepositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, UserAlreadyConfirmed, NoItemsFound, \
    InvalidCredentials, UserNotConfirmed, DuplicatedItem, InvalidTokenError
from src.shared.infra.dto.user_cognito_dto import UserCognitoDTO
from src.shared.infra.services.confirmation_code_mail_html import generate_confirmation_mail


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
        cognito_attributes = [attr for attr in cognito_attributes if attr['Name'] != 'password']
        code = self.generate_confirmation_code()
        cognito_attributes.append({'Name': 'custom:confirmationCode', 'Value': code})
        base_pwd_cognito = Environments.get_envs().base_pwd_cognito
        try:            
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=user.email,
                Password=base_pwd_cognito,
                UserAttributes=cognito_attributes)
            
            print(f'USER REPO COGNITO response CREATE USER {response}')

            user.user_id = response.get("UserSub")
            
            self.send_confirmation_code_mail(user.email, user.name, code)
            
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
        
    def send_confirmation_code_mail(self, to_email: str, name: str, code: str):
        try:
            mailer = emails.NewEmail(os.environ.get('MAILERSEND_API_KEY'))
            
            mail_from = {
                "name": "Dev Dynasty",
                "email": os.environ.get('FROM_EMAIL')
            }
            
            email_to = {
                "name": name,
                "email": to_email
            }
            
            
            reply_to = {
                "name": "Dev Dynasty",
                "email": os.environ.get('REPLY_TO_EMAIL')
            }
            
            confirmation_html = generate_confirmation_mail(code)
            
            mail_body = {}
            
            mailer.set_mail_from({"email": mail_from['email']}, mail_body)
            mailer.set_mail_to([{"email": email_to['email']}], mail_body)
            mailer.set_reply_to([{"email": reply_to['email']}], mail_body)
            mailer.set_html_content(confirmation_html, mail_body)
            mailer.set_subject("Dev Dynasty - Confirmation Code", mail_body)
            
            print(f'MAILER {mailer}')
            print(f'MAIL BODY {mail_body}')
            
            res = mailer.send(mail_body)
            
            print(f'RES MAILER {res}')
            
            return res
        except Exception as e:
            print(f'ERROR MAILER {e}')
            raise ValueError("An error occurred while sending confirmation code mail")
        
        
    def generate_confirmation_code(self):
        return ''.join(random.choices(string.digits, k=6))
    
    def confirm_user(self, email: str, confirmation_code: str):
        try:
            resp = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            
            user_attrs = {attr['Name']: attr['Value'] for attr in resp['UserAttributes']}
            
            print(f'USER REPO COGNITO CONFIRM USER {user_attrs}')
            print(f'USER REPO COGNITO CONFIRM USER {user_attrs.get("custom:confirmation_code")}')
            
            if user_attrs.get('custom:confirmation_code') == confirmation_code:
                self.client.admin_update_user_attributes(
                    UserPoolId=self.user_pool_id,
                    Username=email,
                    UserAttributes=[
                        {'Name': 'email_verified', 'Value': 'true'},
                        {'Name': 'custom:confirmation_code', 'Value': ''}
                    ]
                )
                
                return UserCognitoDTO.from_cognito(resp).to_entity()
            else:
                raise EntityError("confirmation_code")
            
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
            
            
