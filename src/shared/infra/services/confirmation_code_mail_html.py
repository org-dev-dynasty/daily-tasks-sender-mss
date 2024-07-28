def generate_confirmation_mail(code: str):
  code = " ".join(code)
  print(f'CODE GENERATION {code}')
  return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmação de Email</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;600&display=swap">
    <style>
        html, body {{
            height: 100%;
            margin: 0;
        }}
        body {{
            background: linear-gradient(180deg, #3C0B50 0%, #2E083D 28%, #0F0413 100%);
            font-family: 'Jost', sans-serif;
            color: #FFF;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        .logo-top {{
            margin-bottom: 40px;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #ffffff;
            background: linear-gradient(180deg, #3C0B50 0%, #2E083D 28%, #0F0413 100%);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #FFF;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        p {{
            font-size: 16px;
            line-height: 1.5;
        }}
        .code-container {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
            border-radius: 8px;
            padding: 5px;
        }}
        .code-box {{
            width: 40px;
            height: 40px;
            border: 2px solid #F06B41;
            border-radius: 4px;
            margin: 0 5px;
            text-align: center;
            font-size: 24px;
            line-height: 40px;
            font-weight: 600;
        }}
        .copy-btn {{
            display: block;
            width: 100%;
            max-width: 150px;
            margin: 20px auto;
            padding: 10px;
            background-color: #F06B41;
            color: #fff;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
            font-family: 'Jost', sans-serif;
        }}
        .copy-btn:hover {{
            background-color: #B03D18;
        }}
        .popup {{
            display: none;
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #000;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }}
        .popup.show {{
            display: block;
        }}
        .footer {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            font-size: 14px;
            color: #FFF;
        }}
        .footer img {{
            max-width: 100px;
            height: auto;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <img class="logo-top" src="https://i.imgur.com/b5wFIoy.png" alt="Logo Top" style="max-width: 300px; height: auto;">
    <div class="container">
        <h1>Confirme seu Email</h1>
        <p>Olá,</p>
        <p>Obrigado por criar uma conta conosco. Para confirmar seu endereço de email, por favor, use o código abaixo:</p>
        
        <div class="code-container" id="code">
            <div class="code-box">{code[0]}</div>
            <div class="code-box">{code[2]}</div>
            <div class="code-box">{code[4]}</div>
            <div class="code-box">{code[6]}</div>
            <div class="code-box">{code[8]}</div>
            <div class="code-box">{code[10]}</div>
        </div>
        <p>Se você não se registrou em nossa plataforma, por favor, ignore este email.</p>
        
        <div class="footer">
            <img src="https://i.imgur.com/Po269cl.png" alt="Logo DevDynasty">
            <p>&#9400; Todos os direitos são reservados.</p>
        </div>
    </div>
</body>
</html>
"""