from enum import Enum
from typing import List

from src.shared.domain.entities.user import User


class UserCognitoDTO:
    user_id: str
    name: str
    email: str
    phone: str  # with country code
    password: str
    accepted_terms: bool
    accepted_notifications_email: bool

    TO_COGNITO_DICT = {
        "name": "name",
        "email": "email",
        "password": "password",
        "phone": "custom:phone",
        "accepted_terms": "custom:acceptedTerms",
        "accepted_notifications_email": "custom:acceptedNotificationMail",
    }
    FROM_COGNITO_DICT = {value: key for key, value in TO_COGNITO_DICT.items()}
    FROM_COGNITO_DICT["sub"] = "user_id"

    def __init__(self, user_id: str, email: str, name: str, phone: str,
                 password: str = None, accepted_terms: bool = None,
                 accepted_notifications_email: bool = None
                 ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.accepted_terms = accepted_terms
        self.accepted_notifications_email = accepted_notifications_email

    @staticmethod
    def from_entity(user: User):
        return UserCognitoDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=user.password,
            accepted_terms=user.accepted_terms,
            accepted_notifications_email=user.accepted_notifications_email,
        )

    def to_cognito_attributes(self) -> List[dict]:
        user_attributes = [self.parse_attribute(value=getattr(self, att), name=self.TO_COGNITO_DICT[att]) for att in
                           self.TO_COGNITO_DICT]
        user_attributes = [att for att in user_attributes if att["Value"] != str(None)]

        return user_attributes

    @staticmethod
    def from_cognito(data: dict) -> "UserCognitoDTO":
        user_data = next((value for key, value in data.items() if "Attribute" in key), None)

        user_data = {UserCognitoDTO.FROM_COGNITO_DICT[att["Name"]]: att["Value"] for att in user_data if
                     att["Name"] in UserCognitoDTO.FROM_COGNITO_DICT}
        user_data["created_at"] = data.get("UserCreateDate")
        user_data["updated_at"] = data.get("UserLastModifiedDate")

        return UserCognitoDTO(
            user_id=user_data.get("user_id"),
            name=user_data.get("name"),
            email=user_data.get("email"),
            phone=user_data.get("phone"),
            password=None,
            accepted_terms=eval(user_data.get("accepted_terms").title()),
            accepted_notifications_email=eval(user_data.get("accepted_notifications_email").title()),
        )

    def to_entity(self) -> User:
        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            phone=self.phone,
            password=self.password,
            accepted_terms=self.accepted_terms,
            accepted_notifications_email=self.accepted_notifications_email
        )

    def __eq__(self, other):
        return self.user_id == other.user_id and self.email == other.email and self.name == other.name and self.password == other.password and self.accepted_terms == other.accepted_terms and self.accepted_notifications_email == other.accepted_notifications_email and self.phone == other.phone

    @staticmethod
    def parse_attribute(name, value) -> dict:
        return {'Name': name, 'Value': str(value)}

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'accepted_terms': self.accepted_terms,
            'accepted_notifications_email': self.accepted_notifications_email,
        }
