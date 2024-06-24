import abc
import re
from typing import Optional
from uuid import uuid4

from shared.helpers.errors.domain_errors import EntityError

class User(abc.ABC):
  user_id: str
  name: str
  email: str
  phone: str
  password: str
  
  def __init__(self, name: str, email: str, phone: Optional[str], password: str) -> None:
    
    if phone is not None:
      if not self.validate_phone(phone):
        raise EntityError("phone")
      
    if not self.validate_name(name):
      raise EntityError("name")
    
    if not self.validate_email(email):
      raise EntityError("email")
    
    if not self.validate_password(password):
      raise EntityError("password")
    
    self.user_id = str(uuid4())
    self.name = name
    self.email = email
    self.phone = phone
    self.password = password
    
  
  @staticmethod
  def validate_name(name: str) -> bool:
    if len(name) < 2:
      return False
    if name == "":
      return False
    if name is None:
      return False
    return True
  
  @staticmethod
  def validate_email(email: str) -> bool:
    rgx = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    
    if not re.search(rgx, email):
      return False
    if email == "":
      return False
    if email is None:
      return False
    return True
  
  @staticmethod
  def validate_phone(phone: str) -> bool:
    rgx = r'^\d{10,11}$'
    
    if not re.search(rgx, phone):
      return False
    if phone == "":
      return False
    if phone is None:
      return False
    return True
  
  @staticmethod
  def validate_password(password: str) -> bool:
    # do a regex for password validation, 1 upper, 1 lower, 1 number, 1 special char, 6 chars
    
    rgx = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
    
    if not re.search(rgx, password):
      return False
    if password == "":
      return False
    if password is None:
      return False
    return True
    