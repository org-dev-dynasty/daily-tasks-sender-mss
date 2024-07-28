def generate_forgot_password_mail(pwd: str):
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
            position: relative;
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
            align-items: center;
            width: 100%;
            height: 40px;
            background-color: #000;
            color: #fff;
            font-size: 24px;
            text-align: center;
            cursor: pointer;
            border-radius: 4px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }}
        .code-container span {{
            display: none;
            color: #F06B41;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}
        .code-container.active span {{
            display: inline;
        }}
        .code-container.inactive {{
            background-color: transparent;
        }}
        .code-text{{
        	font-size: 24px;
        }}
        .code-text.inactive{{
        	display: none;
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
            flex-direction: row;
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
        <h1>Esqueci a senha</h1>
        <p>Olá,</p>
        <p>Estamos enviando este email em resposta a seu pedido de troca de senha. Aqui está a nova senha da sua conta:</p>
        
        <div class="code-container" id="code-container" onclick="toggleCode()">
            <span id="code">{pwd}</span>
            <p class="code-text" id="code-text">Clique aqui para ver a senha</p>
        </div>

        <button class="copy-btn" onclick="copyCode()">Copiar Senha</button>

        <p>Se quiser alterar esta senha provisória, faça login na sua conta e altere a sua senha nas configurações.</p>
        
        <div class="footer">
            <img src="https://i.imgur.com/Po269cl.png" alt="Logo DevDynasty">
            <p>&#9400; Todos os direitos são reservados.</p>
        </div>
    </div>

    <div class="popup" id="popup">Senha copiada para a área de transferência!</div>

    <script>
        let isCodeVisible = false;

        function toggleCode() {{
            const codeContainer = document.getElementById('code-container');
            const codeText = document.getElementById('code-text');
            if (!isCodeVisible) {{
                codeContainer.classList.add('active');
                codeContainer.classList.add('inactive');
                codeText.classList.add('inactive');
                isCodeVisible = true;
            }}
        }}

        function copyCode() {{
            const code = document.getElementById('code').innerText;
            const textarea = document.createElement('textarea');
            textarea.value = code;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            const popup = document.getElementById('popup');
            popup.classList.add('show');
            setTimeout(() => {{
                popup.classList.remove('show');
            }}, 2000);
        }}
    </script>
</body>
</html>

  """