# src/gmail_utils.py
import os, base64, threading, time
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email import message_from_bytes
from googleapiclient.errors import HttpError
from config import GMAIL_CREDENTIALS, GMAIL_TOKEN

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
OAUTH_IN_PROGRESS = False
OAUTH_TIMEOUT = 120  # 2 minutes timeout for OAuth

def _perform_oauth():
    """Perform OAuth in a separate thread to avoid blocking."""
    global OAUTH_IN_PROGRESS
    try:
        print("🔐 Starting Gmail OAuth authorization...")
        print("📱 A browser window should open. Please complete authorization.")
        
        flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)
        
        print("✅ New Gmail credentials obtained")
        
        try:
            with open(GMAIL_TOKEN, 'w') as token:
                token.write(creds.to_json())
            print("✅ Gmail token saved successfully")
        except Exception as e:
            print(f"⚠️ Error saving token: {e}")
        
    except Exception as e:
        print(f"❌ Gmail OAuth flow error: {e}")
    finally:
        OAUTH_IN_PROGRESS = False

def gmail_auth():
    global OAUTH_IN_PROGRESS
    
    creds = None
    if os.path.exists(GMAIL_TOKEN):
        try:
            creds = Credentials.from_authorized_user_file(GMAIL_TOKEN, SCOPES)
            if creds and creds.valid:
                service = build('gmail', 'v1', credentials=creds)
                return service
        except Exception as e:
            print(f"⚠️ Error loading token file: {e}")
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ Gmail token refreshed successfully")
                service = build('gmail', 'v1', credentials=creds)
                return service
            except Exception as e:
                print(f"⚠️ Token refresh failed: {e}")
                creds = None
        
        # Check if OAuth is already in progress
        if OAUTH_IN_PROGRESS:
            print("⏳ Gmail OAuth authorization in progress... Skipping this scan.")
            return None
        
        if not creds:
            # Start OAuth in a background thread
            if not OAUTH_IN_PROGRESS:
                OAUTH_IN_PROGRESS = True
                oauth_thread = threading.Thread(target=_perform_oauth, daemon=True)
                oauth_thread.start()
            
            print("⏳ Gmail authorization requested. First scan will proceed after authorization completes.")
            return None
    
    return None

def fetch_unread_messages(service, user_id='me', q='is:unread'):
    try:
        results = service.users().messages().list(userId=user_id, q=q).execute()
        msg_ids = results.get('messages', [])
        return msg_ids
    except HttpError as e:
        print("Gmail list error:", e)
        return []

def get_message(service, msg_id, user_id='me'):
    msg = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    raw = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    em = message_from_bytes(raw)
    return em, msg

def add_label(service, msg_id, label_ids=['SPAM'], user_id='me'):
    try:
        body = {'addLabelIds': label_ids}
        service.users().messages().modify(userId=user_id, id=msg_id, body=body).execute()
    except HttpError as e:
        print("Label modify error:", e)
def fetch_unread_emails(max_results=5):
    """
    Fetch unread Gmail messages and return a list of tuples:
    (msg_id, subject, body, attachments)
    """
    service = gmail_auth()
    if not service:
        print("❌ Failed to authenticate with Gmail")
        return []
    
    messages = fetch_unread_messages(service)
    if not messages:
        print("✅ No unread Gmail messages")
        return []

    email_list = []
    for m in messages[:max_results]:
        msg_id = m["id"]
        try:
            msg_data = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")

            # Extract body text
            body = ""
            if "parts" in payload:
                for part in payload["parts"]:
                    mime_type = part.get("mimeType", "")
                    if mime_type == "text/plain":
                        data = part.get("body", {}).get("data")
                        if data:
                            body += base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            else:
                data = payload.get("body", {}).get("data")
                if data:
                    body += base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

            # Extract attachments
            attachments = []
            if "parts" in payload:
                for part in payload["parts"]:
                    if part.get("filename") and "attachmentId" in part.get("body", {}):
                        att_id = part["body"]["attachmentId"]
                        att = service.users().messages().attachments().get(userId="me", messageId=msg_id, id=att_id).execute()
                        file_data = base64.urlsafe_b64decode(att["data"])
                        attachments.append((part["mimeType"], file_data))

            email_list.append((msg_id, subject, body, attachments))

        except Exception as e:
            print(f"⚠️ Error reading message {msg_id}: {e}")

    return email_list
# existing imports stay the same
# add this function at the end of gmail_utils.py

def move_to_spam(msg_id, user_id='me'):
    """
    Move a specific Gmail message to the Spam folder.
    Reuses add_label() to add 'SPAM' label to the message.
    """
    try:
        service = gmail_auth()  # reuse authentication
        body = {'addLabelIds': ['SPAM'], 'removeLabelIds': ['INBOX']}
        service.users().messages().modify(userId=user_id, id=msg_id, body=body).execute()
        print(f"🚨 Message {msg_id} moved to Spam successfully.")
    except Exception as e:
        print(f"❌ Failed to move message {msg_id} to Spam:", e)
