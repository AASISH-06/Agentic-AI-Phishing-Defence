# src/twilio_utils.py
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, ALERT_PHONE

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_alert_sms(message, to=ALERT_PHONE):
    """Send a normal SMS alert."""
    try:
        msg = client.messages.create(
            body=f"🚨 Phishing Alert:\n{message}",
            from_=TWILIO_NUMBER,
            to=to
        )
        print(f"📲 SMS Alert sent successfully to {to}! SID: {msg.sid}")
    except Exception as e:
        print(f"⚠️ Failed to send SMS alert: {e}")

def send_alert_whatsapp(message, recipient):
    """Send a WhatsApp alert via Twilio Sandbox."""
    try:
        if not recipient.startswith("+"):
            recipient = f"+{recipient.lstrip('+')}"
        msg = client.messages.create(
            from_="whatsapp:+14155238886",  # Twilio sandbox WhatsApp number
            to=f"whatsapp:{recipient}",
            body=message
        )
        print(f"✅ WhatsApp alert sent successfully! SID: {msg.sid}")
    except Exception as e:
        print(f"⚠️ Failed to send WhatsApp alert: {e}")
