import abc
import re
from typing import Optional
from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    user_id: Optional[str]
    name: str
    email: str
    phone: Optional[str]
    password: Optional[str]
    accepted_terms: bool
    accepted_notifications_email: bool

    def __init__(
            self,
            name: str,
            email: str,
            phone: Optional[str] = None,
            password: Optional[str] = None,
            accepted_terms: bool = False,
            accepted_notifications_email: bool = False,
            user_id: Optional[str] = None
    ) -> None:

        if user_id is None:
            self.user_id = None
        else:
            self.user_id = user_id

        if not self.validate_phone(phone):
            raise EntityError("phone")

        if not self.validate_name(name):
            raise EntityError("name")

        if not self.validate_email(email):
            raise EntityError("email")

        if not self.validate_password(password):
            raise EntityError("password")

        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.accepted_terms = accepted_terms
        self.accepted_notifications_email = accepted_notifications_email

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        if len(name) < 2:
            return False
        if name == "":
            return False
        if re.search(r'\d', name):
            return False
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        rgx = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+(\.\w+)+$'

        if email is None:
            return False
        if not re.search(rgx, email):
            return False
        if email == "":
            return False
        return True

    @staticmethod
    def validate_phone(phone: Optional[str]) -> bool:
        rgx = r'^\d{11}$'

        if phone is None:
            return True  # Phone is optional, so None is valid
        if phone == "":
            return False
        if not re.search(rgx, phone):
            return False
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        # do a regex for password validation, 1 upper, 1 lower, 1 number, 1 special char, 6 chars

        rgx = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@$!%#*?&]{6,}$'

        if password is None:
            return False
        if not re.search(rgx, password):
            return False
        if password == "":
            return False
        return True

    @staticmethod
    def parse_object(user: dict) -> 'User':
        return User(
            email=user['email'],
            name=user['name'].title(),
            phone=user['phone'] if user.get('phone') is not None else None,
            password=user['password'] if user.get(
                'password') is not None else None,
            accepted_terms=user['accepted_terms'] if user.get(
                'accepted_terms') is not None else None,
            accepted_notifications_email=user['accepted_notifications_email'] if user.get(
                'accepted_notifications_email') is not None else None,
            user_id=user.get("user_id")
        )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'accepted_terms': self.accepted_terms,
            'accepted_notifications_sms': self.accepted_notifications_sms,
            'accepted_notifications_email': self.accepted_notifications_email,
        }
