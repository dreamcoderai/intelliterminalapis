# app/core/email.py

import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def send_otp_email(to_email: str, otp: str, name: str) -> None:
    load_dotenv(_ENV_PATH, override=True)

    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "465").strip())
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()
    from_email = os.getenv("SMTP_FROM", smtp_user).strip()

    if not all([smtp_host, smtp_user, smtp_pass]):
        print(f"[DEV] Password reset OTP for {to_email}: {otp}")
        return

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;background:#0F1E35;border-radius:16px;padding:32px;color:#fff">
      <div style="text-align:center;margin-bottom:24px">
        <span style="color:#22d3ee;font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase">PulseTerminal</span>
      </div>
      <h2 style="margin:0 0 8px;font-size:22px">Password Reset</h2>
      <p style="color:#94a3b8;margin:0 0 24px">Hi {name}, use the OTP below to reset your password. It expires in <strong style="color:#fff">15 minutes</strong>.</p>
      <div style="background:#132743;border:1px solid rgba(34,211,238,0.2);border-radius:12px;padding:24px;text-align:center;margin-bottom:24px">
        <span style="font-size:36px;font-weight:700;letter-spacing:10px;color:#22d3ee">{otp}</span>
      </div>
      <p style="color:#64748b;font-size:12px;margin:0">If you did not request this, you can safely ignore this email. Do not share this OTP with anyone.</p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your PulseTerminal Password Reset OTP"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    # GoDaddy (secureserver.net) serves a certificate that fails strict
    # hostname verification — use a permissive context.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx, timeout=15) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_email, msg.as_string())
    except (smtplib.SMTPConnectError, ssl.SSLError, OSError):
        with smtplib.SMTP(smtp_host, 587, timeout=15) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_email, msg.as_string())
