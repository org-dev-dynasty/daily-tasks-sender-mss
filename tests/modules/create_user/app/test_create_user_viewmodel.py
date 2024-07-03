from src.shared.domain.entities.user import User
from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel

class Test_CreateUserViewmodel:

    def test_get_user_viewmodel(self):
        user = User(
            name='Luca',
            email='luquinha@gmail.com', 
            phone="11991758098",
            password='Teste@01',
            accepted_terms=True,
            accepted_notifications_email=True
        )

        expected = {
            'user': {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            },
            'message': 'the user was created'
        }

        viewmodel = CreateUserViewmodel(user)

        assert viewmodel.to_dict() == expected
