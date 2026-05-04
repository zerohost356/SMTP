import smtplib
import random
import dns.resolver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "bot@yourdomain.com"
RECEIVER_EMAIL = "deirdre78ae9d@un.accesswiki.net"


def generate_otp():
    return str(random.randint(100000, 999999))


def get_mx_host(domain):
    records = dns.resolver.resolve(domain, "MX")
    mx_host = sorted(records, key=lambda r: r.preference)[0].exchange.to_text().rstrip(".")
    return mx_host


def send_direct(receiver_email, otp_code):
    domain = receiver_email.split("@")[1]

    try:
        mx_host = get_mx_host(domain)
        print(f"[INFO] MX record: {mx_host}")
    except Exception as e:
        print(f"[LỖI] Không tìm được MX record: {e}")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Discord Bot - Mã OTP xác minh"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    body = f"""\
Xin chào,

Mã OTP xác minh Discord của bạn là:

    {otp_code}

Mã này có hiệu lực trong 5 phút.
Không chia sẻ mã này với bất kỳ ai.

- Discord Bot
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(mx_host, 25, timeout=10) as server:
            server.ehlo("yourdomain.com")
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        print(f"[OK] Đã gửi OTP {otp_code} tới {receiver_email}")
        return True
    except Exception as e:
        print(f"[LỖI] Gửi thất bại: {e}")
        return False


if __name__ == "__main__":
    otp = generate_otp()
    send_direct(RECEIVER_EMAIL, otp)
