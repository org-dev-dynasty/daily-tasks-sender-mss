from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User


class Test_GetAllUsersViewmodel:
    all_users_list = [
        User(
            name="Almeida Junior",
            email="almeida.junior@email.com",
            phone="1234538232",
            password="CudeGalinha@02"
        ),
        User(
            name="Papa Francisco",
            email="papa.francisco@email.com",
            phone="1334538232",
            password="Igr3J4@01"
        )
    ]

    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(self.all_users_list)

        expected = {
            "users": [
                {
                    'user_id': self.all_users_list[0].user_id,
                    'name': "Almeida Junior",
                    'email': "almeida.junior@email.com",
                    'phone': "1234538232",
                    'password': "CudeGalinha@02"
                },
                {
                    'user_id': self.all_users_list[1].user_id,
                    'name': "Papa Francisco",
                    'email': "papa.francisco@email.com",
                    'phone': "1334538232",
                    'password': "Igr3J4@01"
                }
            ],
            "message": "All users have been retrieved successfully!"
        }

        response = viewmodel.to_dict()

        assert response == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(
            user_id=self.all_users_list[0].user_id,
            name="Antonito Constante",
            email="antonito.constante@email.com",
            phone="1234538223",
            password="CudeGalinha@02"
        )

        response = viewmodel.to_dict()

        expected = {
                    'user_id': self.all_users_list[0].user_id,
                    'name': "Antonito Constante",
                    'email': "antonito.constante@email.com",
                    'phone': "1234538223",
                    'password': "CudeGalinha@02"
        }

        assert response == expected
