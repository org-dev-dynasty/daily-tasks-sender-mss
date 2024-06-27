import pytest
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError


class Test_User:
  def test_entity_correctly(self):
    user = User(name='Gabriel', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')

    assert type(user) == User
    assert user.name == 'Gabriel'
    assert user.email == 'gabrielmerola@gmail.com'
    assert user.phone == '11912345678'
    assert user.password == 'Teste@01'

  def test_entity_incorrectly_name(self):
    with pytest.raises(EntityError):
      User(name='Gabriel123', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
    with pytest.raises(EntityError):
      User(name='', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
    with pytest.raises(EntityError):
      User(name=None, email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
    with pytest.raises(EntityError):
      User(name='a', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
  
  def test_entity_incorrectly_email(self):
    with pytest.raises(EntityError):
      User(name='Luca', email='lucajamesmail.com', phone='11912345678', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email='luca james@mailcom', phone='11912345678', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email='', phone='11912345678', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email=None, phone='11912345678', password='LucaoXuxu@01')

  def test_entity_incorrectly_phone(self):
    with pytest.raises(EntityError):
      User(name='Luca', email='lucajames@gmail.com', phone='119123456789', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email='lucajames@gmail.com', phone='1191234567', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email='lucajames@gmail.com', phone='jojo', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email='lucajames@gmail.com', phone='', password='LucaoXuxu@01')
    with pytest.raises(EntityError):
      User(name='Luca', email='lucajames@gmail.com', phone=None, password='LucaoXuxu@01')
  
  def test_entity_incorrectly_password(self):
    with pytest.raises(EntityError):
      User(name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='rodinizin12')
    with pytest.raises(EntityError):
      User(name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='123123')
    with pytest.raises(EntityError):
      User(name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='(@!*#&$*!@#)')
    with pytest.raises(EntityError):
      User(name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='')
    with pytest.raises(EntityError):
      User(name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password=None)
  