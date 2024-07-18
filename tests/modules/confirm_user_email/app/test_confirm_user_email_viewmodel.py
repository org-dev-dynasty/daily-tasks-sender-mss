from src.shared.domain.entities.user import User
from src.modules.confirm_user_email.app.confirm_user_email_viewmodel import ConfirmUserEmailViewmodel

class Test_ConfirmUserEmailViewmodel:

    def test_confirm_user_viewmodel(self):
        expected = {
          'message': 'User email has been confirmed'
        }

        viewmodel = ConfirmUserEmailViewmodel()

        assert viewmodel.to_dict() == expected
