def generate_confirmation_mail(code: str):
  return f"""
  <html>
  <body>
  <h1>Dev Dynasty</h1>
  <p>Your confirmation code is: {code}</p>
  </body>
  </html>
  """
