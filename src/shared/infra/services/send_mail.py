import os
from mailersend import emails
from src.shared.infra.services.confirmation_code_mail_html import generate_confirmation_mail
from src.shared.infra.services.forgot_password_mail_html import generate_forgot_password_mail


def send_confirmation_code_mail(to_email: str, code: str):
    try:
        mailer = emails.NewEmail(os.environ.get('MAILERSEND_API_KEY'))
        
        domain_mail = os.environ.get('FROM_EMAIL')
        reply_to_email = os.environ.get('REPLY_TO_EMAIL')
        
        mail_from = {
            "name": "Dev Dynasty",
            "email": "noreply@trial-351ndgw81vqgzqx8.mlsender.net"
        }
        
        email_to = {
            "email": to_email
        }
        
        
        reply_to = {
            "name": "Dev Dynasty",
            "email": "reply@trial-351ndgw81vqgzqx8.mlsender.net"
        }
        
        confirmation_html = generate_confirmation_mail(code)
        
        mail_body = {}
        
        mailer.set_mail_from({"email": mail_from['email']}, mail_body)
        mailer.set_mail_to([{"email": email_to['email']}], mail_body)
        mailer.set_reply_to([{"email": reply_to['email']}], mail_body)
        mailer.set_html_content(confirmation_html, mail_body)
        mailer.set_subject("Dev Dynasty - Código de verificação de email", mail_body)
        
        print(f'MAILER {mailer}')
        print(f'MAIL BODY {mail_body}')
        
        res = mailer.send(mail_body)
        
        print(f'RES MAILER {res}')
        
        return res
    except Exception as e:
        print(f'ERROR MAILER {e}')
        raise ValueError("An error occurred while sending confirmation code mail")
        
def send_forgot_pwd_mail(to_email: str, gen_pwd: str):
    try:
        mailer = emails.NewEmail(os.environ.get('MAILERSEND_API_KEY'))
        
        domain_mail = os.environ.get('FROM_EMAIL')
        reply_to_email = os.environ.get('REPLY_TO_EMAIL')
        
        mail_from = {
            "name": "Dev Dynasty",
            "email": "noreply@trial-351ndgw81vqgzqx8.mlsender.net"
        }
        
        email_to = {
            "email": to_email
        }
        
        
        reply_to = {
            "name": "Dev Dynasty",
            "email": "reply@trial-351ndgw81vqgzqx8.mlsender.net"
        }
        
        forgot_pwd_html = generate_forgot_password_mail(gen_pwd)
        
        mail_body = {}
        
        mailer.set_mail_from({"email": mail_from['email']}, mail_body)
        mailer.set_mail_to([{"email": email_to['email']}], mail_body)
        mailer.set_reply_to([{"email": reply_to['email']}], mail_body)
        mailer.set_html_content(forgot_pwd_html, mail_body)
        mailer.set_subject("Dev Dynasty - Recuperação de senha", mail_body)
        
        print(f'MAILER {mailer}')
        print(f'MAIL BODY {mail_body}')
        
        res = mailer.send(mail_body)
        
        print(f'RES MAILER {res}')
        
        return res
    except Exception as e:
        print(f'ERROR MAILER {e}')
        raise ValueError("An error occurred while sending confirmation code mail")