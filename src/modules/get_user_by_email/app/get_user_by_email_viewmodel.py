from typing import Optional
from src.shared.domain.entities.user import User

class GetUserByEmailViewmodel:
    id: str
    name: str
    email: str
    phone: Optional[str]
    password: str

    def __init__(self, user: User) -> None:
        self.id = user.user_id
        self.name = user.name
        self.email = user.email
        self.phone = user.phone
        self.password = user.password
