# app/core/email.py

import os
from pathlib import Path

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def send_otp_email(to_email: str, otp: str, name: str) -> None:
    load_dotenv(_ENV_PATH, override=True)

    api_key = os.getenv("SENDGRID_API_KEY", "").strip()
    from_email = os.getenv("SMTP_FROM", "").strip()

    if not api_key:
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

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject="Your PulseTerminal Password Reset OTP",
        html_content=html,
    )
    SendGridAPIClient(api_key).send(message)
