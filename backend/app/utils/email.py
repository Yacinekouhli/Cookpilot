import os
import resend

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM", "Cookpilot <no-reply@example.com>")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


def send_verification_email(to_email: str, token: str):
    """
    Envoie un e-mail avec un lien vers le frontend (ou backend) pour vérifier l'adresse.
    """
    verify_url = f"{FRONTEND_BASE_URL}/verify-email?token={token}"
    html = f"""
    <p>Welcome to Cookpilot!</p>
    <p>Please verify your email by clicking this link:</p>
    <p><a href="{verify_url}">{verify_url}</a></p>
    <p>This link expires in 24 hours.</p>
    """

    if not RESEND_API_KEY:
        # Dev fallback: log en console
        print(f"[DEV] Send email to {to_email} with link: {verify_url}")
        return

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [to_email],
        "subject": "Verify your Cookpilot account",
        "html": html
    })
