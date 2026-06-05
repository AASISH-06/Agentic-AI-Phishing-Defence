# src/app.py
from flask import Flask, request, jsonify, render_template
from threading import Thread
from twilio.twiml.messaging_response import MessagingResponse
from analyzer import analyze_text
from ocr_utils import image_to_text
from stego import extract_lsb_text_from_image_bytes
import worker
import requests, io
from PIL import Image
from flask import Flask, render_template
from logger_db import fetch_all_scans, init_db
from logger_db import log_scan
from twilio_utils import send_alert_whatsapp
import webbrowser
import threading

app = Flask(__name__, template_folder="templates")


# ✅ Flask 3.x fix — launch background scheduler manually
def start_background():
    """Start the background phishing-defense agent."""
    try:
        t = Thread(target=lambda: worker.start_scheduler(interval=worker_interval()))
        t.daemon = True
        t.start()
        print("✅ Background worker started successfully.")
    except Exception as e:
        print("❌ Failed to start background worker:", e)


def worker_interval():
    """Pull scan interval from config if available."""
    try:
        from config import POLL_INTERVAL
        return POLL_INTERVAL
    except Exception:
        return 60


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/twilio/incoming", methods=["GET", "POST"])
def twilio_incoming():
    """
    Handles incoming WhatsApp or SMS messages from Twilio Sandbox.
    Detects platform, analyzes risk, logs result, and sends a reply.
    """
    from flask import request, render_template_string
    from analyzer import analyze_text
    from logger_db import log_scan
    from twilio_utils import send_alert_whatsapp, send_alert_sms

    # ✅ Handle GET (for browser access)
    if request.method == "GET":
     return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>Twilio Webhook Tester</title>
      <style>
        :root {
          --bg1: #0f172a;
          --bg2: #111827;
          --accent1: #06b6d4;
          --accent2: #7c3aed;
          --card: #ffffff;
        }
        body {
          margin: 0;
          font-family: 'Inter', sans-serif;
          background: radial-gradient(circle at 10% 20%, rgba(6,182,212,0.1), transparent 20%),
                      radial-gradient(circle at 90% 80%, rgba(124,58,237,0.1), transparent 25%),
                      linear-gradient(180deg,var(--bg1),var(--bg2));
          color: #f9fafb;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }
        .card {
          background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(250,250,250,0.9));
          color: #111827;
          padding: 40px 50px;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.6);
          transform: perspective(800px) rotateY(-5deg);
          transition: transform 0.3s ease;
          width: 500px;
        }
        .card:hover { transform: perspective(800px) rotateY(0deg) translateY(-5px); }
        h2 {
          font-size: 1.6rem;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        h2 span {
          background: linear-gradient(135deg, var(--accent1), var(--accent2));
          color: white;
          font-weight: bold;
          border-radius: 50%;
          padding: 8px 10px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        p { color: #334155; font-size: 0.95rem; line-height: 1.5; }
        label { font-weight: 600; color: #0f172a; display: block; margin-top: 20px; }
        input, textarea {
          width: 100%;
          margin-top: 8px;
          padding: 10px;
          font-size: 0.95rem;
          border-radius: 10px;
          border: 1px solid #cbd5e1;
          box-shadow: inset 0 2px 3px rgba(0,0,0,0.05);
        }
        textarea { resize: none; height: 100px; }
        button {
          margin-top: 25px;
          width: 100%;
          background: linear-gradient(90deg, var(--accent2), var(--accent1));
          color: white;
          font-weight: 600;
          border: none;
          border-radius: 12px;
          padding: 12px 0;
          font-size: 1rem;
          cursor: pointer;
          box-shadow: 0 8px 20px rgba(124,58,237,0.35);
          transition: all 0.2s ease;
        }
        button:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 24px rgba(6,182,212,0.4);
        }
        .note {
          margin-top: 20px;
          font-size: 0.85rem;
          color: #475569;
          text-align: center;
        }
      </style>
    </head>
    <body>
      <div class="card">
        <h2><span>✔</span> Twilio Webhook Endpoint Active</h2>
        <p>This endpoint is now ready to receive <b>POST</b> requests from Twilio (WhatsApp only).</p>
        <p>Send a test WhatsApp message from your sandbox or use the form below to simulate one.</p>

        <form method="POST">
          <label>Sender (From):</label>
          <input name="From" placeholder="whatsapp:+911234567890" value="whatsapp:+91" required>

          <label>Message (Body):</label>
          <textarea name="Body" placeholder="Type your test phishing message here..." required>
Your bank account is locked. Verify here: http://secure-login.net
          </textarea>

          <button type="submit">🚀 Send Test POST</button>
        </form>

        <p class="note">💡 Works with WhatsApp Sandbox only. SMS requires Twilio A2P registration.</p>
      </div>
    </body>
    </html>
    """)


    # ✅ Handle POST (Twilio webhook)
    try:
        sender = request.form.get("From", "")
        body = request.form.get("Body", "").strip()

        if not body:
            return "No message content", 400

        # Detect platform
        if "whatsapp:" in sender:
            platform = "WhatsApp"
            recipient = sender.replace("whatsapp:", "")
        else:
            platform = "SMS"
            recipient = sender

        # Analyze text and calculate risk
        result = analyze_text(body)
        risk_score = result.get("risk_score", 0.0)

        print(f"📩 Incoming message from {sender} ({platform})")
        print(f"🧠 NLP={result.get('nlp_score',0)}, OCR={result.get('ocr_detected',False)}, Risk={risk_score}")

        # Log into DB
        log_scan(platform, sender, "Twilio Message", body, risk_score)

        # Generate alert
        if risk_score >= 60:
            alert_message = f"🚨 Phishing Alert! Risk Score: {risk_score:.2f}\nAvoid clicking any links!"
        else:
            alert_message = "✅ Message appears safe."

        # Send alert
        if platform == "WhatsApp":
            send_alert_whatsapp(alert_message, recipient)
        else:
            send_alert_sms(alert_message, recipient)

        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Message Processed - Agentic AI Defence</title>
  <style>
    * {
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
    }
    body {
      margin: 0;
      background: radial-gradient(circle at 10% 20%, rgba(6,182,212,0.2), transparent 20%),
                  radial-gradient(circle at 90% 80%, rgba(124,58,237,0.2), transparent 25%),
                  linear-gradient(135deg, #0f172a, #1e293b);
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      color: #f8fafc;
      overflow: hidden;
    }
    .card {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 20px;
      padding: 40px 60px;
      text-align: center;
      backdrop-filter: blur(12px);
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      animation: fadeIn 1s ease forwards;
      transform: perspective(800px) rotateX(-5deg);
      transition: all 0.3s ease;
    }
    .card:hover {
      transform: perspective(800px) rotateX(0deg) translateY(-3px);
      box-shadow: 0 30px 80px rgba(6,182,212,0.35);
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .checkmark {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      background: linear-gradient(135deg, #06b6d4, #7c3aed);
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0 auto 20px;
      box-shadow: 0 0 40px rgba(124,58,237,0.6);
      animation: pulse 1.5s infinite ease-in-out;
    }
    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 40px rgba(124,58,237,0.6); }
      50% { box-shadow: 0 0 60px rgba(6,182,212,0.9); }
    }
    .checkmark svg {
      width: 55px;
      height: 55px;
      stroke: #fff;
      stroke-width: 5;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      stroke-dasharray: 80;
      stroke-dashoffset: 80;
      animation: draw 1.5s ease forwards;
    }
    @keyframes draw {
      to { stroke-dashoffset: 0; }
    }
    h2 {
      font-size: 1.8rem;
      font-weight: 600;
      margin-bottom: 10px;
      background: linear-gradient(90deg, #06b6d4, #7c3aed);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    p {
      color: #cbd5e1;
      font-size: 1rem;
      line-height: 1.6;
    }
    .button {
      margin-top: 25px;
      display: inline-block;
      background: linear-gradient(90deg, #7c3aed, #06b6d4);
      color: white;
      padding: 12px 28px;
      border-radius: 10px;
      font-weight: 600;
      text-decoration: none;
      box-shadow: 0 10px 30px rgba(6,182,212,0.4);
      transition: all 0.3s ease;
    }
    .button:hover {
      box-shadow: 0 15px 40px rgba(124,58,237,0.6);
      transform: translateY(-3px);
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="checkmark">
      <svg viewBox="0 0 52 52">
        <path d="M14 27l7 7 17-17" />
      </svg>
    </div>
    <h2>Message Processed Successfully</h2>
    <p>Your WhatsApp message was analyzed by the Agentic AI Phishing Defence system.</p>
    <p><strong>Status:</strong> Alert successfully generated and response sent to Twilio Sandbox.</p>
    <a href="/" class="button">⬅ Back to Dashboard</a>
  </div>
</body>
</html>
""")


    except Exception as e:
        print(f"❌ Error in Twilio incoming handler: {e}")
        return str(e), 500

@app.route("/dashboard")
def dashboard():
    from logger_db import fetch_logs  # function that returns (scans, sms_logs)
    scans, sms_logs = fetch_logs()
    return render_template("dashboard.html", scans=scans, sms_logs=sms_logs)

if __name__ == "__main__":
    from worker import start_scheduler

    # Start background Gmail + WhatsApp scan every 60 seconds
    start_scheduler(interval=60)

    # Auto-open dashboard in browser
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")

    # Run Flask app
    app.run(debug=True, use_reloader=False)

