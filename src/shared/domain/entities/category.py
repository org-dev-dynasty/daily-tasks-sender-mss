import uuid
import abc
from typing import Optional

from src.shared.helpers.errors.domain_errors import EntityError

class Category(abc.ABC):
    category_id: Optional[str]
    user_id: str
    category_name: Optional[str]
    category_primary_color: str
    category_secondary_color: str

    def __init__(
            self,
            category_name: Optional[str],
            user_id: str,
            category_primary_color: str,
            category_secondary_color: str,
            category_id: Optional[str]
    ):
        if category_id is None:
            self.category_id = uuid.uuid4().hex
        else:
            self.category_id = category_id
        
        if not user_id:
            raise EntityError("user_id")
        else:
            self.user_id = user_id
        
        if category_name is not None:
            if not self.validate_name(category_name):
                raise EntityError("category_name")
            self.category_name = category_name
        
        if not self.validate_color(category_primary_color):
            raise EntityError("category_primary_color")
        
        if not self.validate_color(category_secondary_color):
            raise EntityError("category_secondary_color")
        
        self.category_name = category_name
        self.category_primary_color = category_primary_color
        self.category_secondary_color = category_secondary_color
    
    @staticmethod
    def validate_name(category_name: str) -> bool:
        if len(category_name) < 2:
            return False
        if len(category_name) == "":
            return False
        return True
    
    @staticmethod
    def validate_color(color: str) -> bool:
        if not color:
            return False
        if len(color) < 4:
            return False
        if len(color) > 9:
            return False
        if color[0] != "#":
            return False
        if len(color) == "":
            return False
        return True

    def parse_object(category: dict) -> 'Category':
        return Category(
            category_name=category.get("category_name"),
            user_id=category.get("user_id"),
            category_primary_color=category.get("category_primary_color"),
            category_secondary_color=category.get("category_secondary_color"),
            category_id=category.get("category_id")
        )
    
    def to_dict(self) -> dict:
        return {
            "_id": self.category_id,
            "user_id": self.user_id,
            "category_name": self.category_name,
            "category_primary_color": self.category_primary_color,
            "category_secondary_color": self.category_secondary
        }