import os
from app.config import settings

def send_email(to: str, subject: str, body: str) -> None:
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        print(f"[EMAIL LOG] To: {to}\nSubject: {subject}\n{body}\n")
        return
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        message = Mail(from_email='noreply@psicomvp.app', to_emails=to, subject=subject, plain_text_content=body)
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"[EMAIL SENDGRID] {response.status_code} to {to}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
