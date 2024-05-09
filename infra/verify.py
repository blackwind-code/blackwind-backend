import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode
import uuid

def generate_verify_token(): #개인의 식별 토큰을 생성하기 위한 함수
    uid = uuid.uuid4() #랜덤 토큰 생성
    base64_uuid = base64.b64encode(uid.bytes) #base64로 인코딩

    return base64_uuid.decode() #decode된 값을 return

def generate_verify_email_html(url, verfiy_token): #디지 메일로 가는 내용을 정의하는 함수(개인의 토큰과)
    params = {
        'token': verfiy_token
    }
    query = urlencode(params) #개인의 토큰을 url로서 사용할 수 있게 자료형을 바꿔준다
    html = f"""<a href="{url}?{query}">Verify</a>"""

    return html

def generate_verify_email_message(username_to, mail_to, verify_token): # 메일을 보냄!
    message = MIMEMultipart()
    message["From"] = 'BlackwindSystem'
    message["To"] = f'{username_to}님<{mail_to}>'
    message["Subject"] = "Verify Mail to sign up Blckwind Service"

    url = 'http://localhost:8000/verify'
    html = generate_verify_email_html(url, verify_token)
    message.attach(MIMEText(html, "html"))

    return message
