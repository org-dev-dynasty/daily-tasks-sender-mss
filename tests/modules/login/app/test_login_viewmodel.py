# from src.modules.login.app.login_viewmodel import DoLoginViewmodel, LoginViewmodel
# from src.shared.domain.entities.user import User


# class Test_LoginViewmodel:
#     all_users_list = [
#         User(
#             name="Almeida Junior",
#             email="almeida.junior@email.com",
#             phone="1234538232",
#             password="CudeGalinha@02"
#         )
#     ]
#     # FIXME: Corrijir este método, ele não está conseguindo fazer a comparação, o retorno é user: [<src.shared.domain.entities.user.User object at 0x000002A463E9BA40>]
#     def test_get_all_users_viewmodel(self):
#         viewmodel = DoLoginViewmodel(self.all_users_list[0])

#         expected = {
#             "user": [
#                 {
#                     'user_id': self.all_users_list[0].user_id,
#                     'name': "Almeida Junior",
#                     'email': "almeida.junior@email.com",
#                     'phone': "1234538232",
#                     'password': "CudeGalinha@02"
#                 }
#             ],
#             "message": "User logged!"
#         }

#         response = viewmodel.to_dict()

#         assert response == expected

#     def test_user_viewmodel(self):
#         viewmodel = LoginViewmodel(
#             email="antonito.constante@email.com",
#             password="CudeGalinha@02"
#         )

#         response = viewmodel.to_dict()

#         expected = {
#                     'email': "antonito.constante@email.com",
#                     'password': "CudeGalinha@02"
#         }

#         assert response == expected
