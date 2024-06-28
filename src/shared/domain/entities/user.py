import abc
import re
from typing import Optional
from uuid import uuid4

from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    user_id: Optional[str]
    name: str
    email: str
    phone: Optional[str]
    password: str
    accepted_terms: bool
    accepted_notifications_email: bool
    accepted_notifications_sms: bool

    def __init__(
            self,
            user_id: Optional[str],
            name: str,
            email: str,
            phone: Optional[str],
            password: str,
            accepted_terms: bool,
            accepted_notifications_sms: bool,
            accepted_notifications_email: bool
    ) -> None:

        if user_id is None:
            self.user_id = str(uuid4())
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

        if not isinstance(accepted_terms, bool):
            raise EntityError("accepted_terms")

        if not isinstance(accepted_notifications_email, bool):
            raise EntityError("accepted_notifications_email")

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
        rgx = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

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
