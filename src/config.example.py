# src/config.example.py
# This is an EXAMPLE file. Rename to config.py and fill in your actual credentials

import os
from dotenv import load_dotenv

load_dotenv()

# 🧠 Database file path (for logs)
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "scans.db")

# 🧩 Twilio credentials (fill in with your actual ones)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxx")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_auth_token")

# Twilio number for WhatsApp alerts
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", "whatsapp:+1234567890")

# Your phone number (destination for alerts)
ALERT_PHONE = os.getenv("ALERT_PHONE", "whatsapp:+91XXXXXXXXXX")

# Risk threshold (above this, alert is sent)
RISK_THRESHOLD = int(os.getenv("RISK_THRESHOLD", "50"))

# Gmail credentials path
GMAIL_CREDENTIALS = os.getenv("GMAIL_CREDENTIALS", "credentials.json")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN_PATH", "token.json")

# Poll interval for Gmail scanning (in seconds)
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))

print("✅ Configuration loaded from environment variables")
