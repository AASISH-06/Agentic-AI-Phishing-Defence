# src/worker.py
import io, signal, sys, threading
from PIL import Image
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from analyzer import nlp_predict, ocr_keyword_flag, compute_risk_score
from ocr_utils import image_to_text
from stego import extract_lsb_text_from_image_bytes
from gmail_utils import fetch_unread_emails, move_to_spam
import os, json
from logger_db import log_scan
from twilio_utils import send_alert_whatsapp

SCANNED_FILE = "scanned_ids.json"

def load_scanned_ids():
    if os.path.exists(SCANNED_FILE):
        with open(SCANNED_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_scanned_ids(scanned):
    with open(SCANNED_FILE, "w") as f:
        json.dump(list(scanned), f)

# Store processed message IDs (avoid duplicates)
processed_ids = set()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler_lock = threading.Lock()

def process_gmail_message(msg_id, subject, payload_text, attachments):
    """Scan a Gmail message for phishing or steganographic content."""
    combined_text = f"{subject}\n{payload_text}"

    # NLP Phishing check
    nlp_score, nlabel = nlp_predict(combined_text)
    ocr_flag, ocr_found = ocr_keyword_flag(combined_text)

    # Steganography detection
    stego_flag = False
    stego_payloads = []

    for (ctype, bdata) in attachments:
        try:
            img = Image.open(io.BytesIO(bdata))
            txt = image_to_text(img)
            if txt and txt.strip():
                combined_text += "\n" + txt

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            payload = extract_lsb_text_from_image_bytes(img_byte_arr.getvalue())
            if payload and payload.strip():
                stego_flag = True
                stego_payloads.append(payload)
        except Exception as e:
            print("Attachment parse error:", e)

    final_score = compute_risk_score(nlp_score, ocr_flag, stego_flag)

    print(f"\n📧 Message {msg_id} — {subject}")
    print(f"🧠 NLP Score: {nlp_score:.2f}")
    print(f"🔍 OCR Keywords: {ocr_found}")
    print(f"🕵️ Stego Found: {stego_flag}")
    print(f"⚡ Risk Score: {final_score:.2f}\n")

    # Log to database
    log_scan("Gmail", "Unknown", subject, payload_text[:300], final_score)

    # Send alert if risky
    if final_score >= 50:
        move_to_spam(msg_id)
        alert_msg = f"High Risk Gmail Message Detected!\nSubject: {subject}\nScore: {final_score:.2f}"
        send_alert_whatsapp(alert_msg)
        print(f"🚨 WhatsApp alert sent! Risk={final_score:.2f}")

    return {"id": msg_id, "risk": final_score}



def scan_gmail_messages():
    from gmail_utils import OAUTH_IN_PROGRESS
    
    print(f"[{datetime.now()}] 📬 Running Gmail phishing scan...")
    
    # Skip if OAuth is in progress
    if OAUTH_IN_PROGRESS:
        print("⏳ Gmail OAuth still in progress... skipping this scan. Please complete browser authorization.")
        return

    try:
        unread_emails = fetch_unread_emails()
        if not unread_emails:
            print("✅ No new Gmail messages found.")
            return

        scanned_ids = load_scanned_ids()
        new_scanned = set()

        for msg_id, subject, body, attachments in unread_emails:
            if msg_id in scanned_ids:
                continue  # skip previously processed ones
            result = process_gmail_message(msg_id, subject, body, attachments)
            new_scanned.add(msg_id)

            if result["risk"] >= 50:
                from gmail_utils import move_to_spam
                move_to_spam(msg_id)

        # merge old and new
        save_scanned_ids(scanned_ids | new_scanned)
        print(f"✅ Scan complete. Processed {len(new_scanned)} new messages.")

    except Exception as e:
        print("❌ Error during Gmail scan:", e)


def start_scheduler(interval=60):
    """Start the background phishing defense scheduler."""
    print(f"🕒 Starting Agentic AI Phishing Defense every {interval}s...")
    scheduler.add_job(scan_gmail_messages, "interval", seconds=interval, id="gmail_scan", replace_existing=True)
    scheduler.start()


def stop_scheduler(signal, frame):
    """Gracefully stop when user presses Ctrl+C."""
    print("\n🛑 Stopping background scheduler...")
    try:
        if scheduler.running:
            scheduler.shutdown(wait=False)
        else:
            print("⚠️ Scheduler was already stopped.")
    except Exception as e:
        print(f"⚠️ Error during scheduler shutdown: {e}")
    finally:
        sys.exit(0)


# Attach Ctrl+C handler
signal.signal(signal.SIGINT, stop_scheduler)
signal.signal(signal.SIGTERM, stop_scheduler)
