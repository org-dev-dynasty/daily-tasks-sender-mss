import pytest
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError


class Test_User:
    def test_entity_correctly(self):
        user = User(user_id='123', name='Gabriel', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')

        assert type(user) == User
        assert user.user_id == '123'
        assert user.name == 'Gabriel'
        assert user.email == 'gabrielmerola@gmail.com'
        assert user.phone == '11912345678'
        assert user.password == 'Teste@01'

    def test_entity_incorrectly_name(self):
        with pytest.raises(EntityError):
            User(user_id='124', name='Gabriel123', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
        with pytest.raises(EntityError):
            User(user_id='125', name='', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
        with pytest.raises(EntityError):
            User(user_id='126', name=None, email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')
        with pytest.raises(EntityError):
            User(user_id='127', name='a', email='gabrielmerola@gmail.com', phone='11912345678', password='Teste@01')


    def test_entity_incorrectly_email(self):
        with pytest.raises(EntityError):
            User(user_id='128', name='Luca', email='lucajamesmail.com', phone='11912345678', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='129', name='Luca', email='luca james@mailcom', phone='11912345678', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='130', name='Luca', email='', phone='11912345678', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='131', name='Luca', email=None, phone='11912345678', password='LucaoXuxu@01')

    def test_entity_incorrectly_phone(self):
        with pytest.raises(EntityError):
            User(user_id='132', name='Luca', email='lucajames@gmail.com', phone='119123456789', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='133', name='Luca', email='lucajames@gmail.com', phone='1191234567', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='134', name='Luca', email='lucajames@gmail.com', phone='jojo', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='135', name='Luca', email='lucajames@gmail.com', phone='', password='LucaoXuxu@01')
        with pytest.raises(EntityError):
            User(user_id='136', name='Luca', email='lucajames@gmail.com', phone=None, password='LucaoXuxu@01')

    def test_entity_incorrectly_password(self):
        with pytest.raises(EntityError):
            User(user_id='137', name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='rodinizin12')
        with pytest.raises(EntityError):
            User(user_id='138', name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='123123')
        with pytest.raises(EntityError):
            User(user_id='139', name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='(@!*#&$*!@#)')
        with pytest.raises(EntityError):
            User(user_id='140', name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password='')
        with pytest.raises(EntityError):
            User(user_id='141', name='Rodrigo', email='Rodrigo@gmail.com', phone='11912345678', password=None)
