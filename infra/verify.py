import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode
import uuid

def generate_verify_token():
    uid = uuid.uuid4()
    base64_uuid = base64.b64encode(uid.bytes)

    return base64_uuid.decode()

def generate_verify_email_html(url, verfiy_token):
    params = {
        'token': verfiy_token
    }
    query = urlencode(params)
    html = f"""<a href="{url}?{query}">Verify</a>"""

    return html

def generate_verify_email_message(username_to, mail_to, verify_token):
    message = MIMEMultipart()
    message["From"] = 'BlackwindSystem'
    message["To"] = f'{username_to}님<{mail_to}>'
    message["Subject"] = "Verify Mail to sign up Blckwind Service"

    url = 'http://localhost:8000/verify'
    html = generate_verify_email_html(url, verify_token)
    message.attach(MIMEText(html, "html"))

    return message
