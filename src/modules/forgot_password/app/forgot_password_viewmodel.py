class ForgotPasswordViewmodel:
  def to_dict(self):
    return {
      'message': 'Um email foi enviado para você com as instruções para redefinir sua senha'
    }