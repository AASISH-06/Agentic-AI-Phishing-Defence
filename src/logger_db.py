# src/logger_db.py
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "scans.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            sender TEXT,
            subject TEXT,
            message TEXT,
            risk_score REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_scan(platform, sender, subject, message, risk_score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO scans (platform, sender, subject, message, risk_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (platform, sender, subject, message, risk_score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def fetch_all_scans():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM scans ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_logs():
    """
    Fetch Gmail and SMS/WhatsApp logs separately for dashboard display.
    Reuses existing 'scans' table.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        # Fetch Gmail logs
        c.execute("SELECT * FROM scans WHERE platform = 'Gmail' ORDER BY id DESC LIMIT 50")
        scans = c.fetchall()

        # Fetch SMS / WhatsApp logs
        c.execute("SELECT * FROM scans WHERE platform IN ('SMS', 'WhatsApp') ORDER BY id DESC LIMIT 50")
        sms_data = c.fetchall()

        # Convert SMS/WhatsApp data into dictionary format for HTML table
        sms_logs = []
        for row in sms_data:
            sms_logs.append({
                "sender": row[2],
                "message": row[4],
                "risk": row[5]
            })

        return scans, sms_logs

    except Exception as e:
        print("⚠️ Error while fetching logs:", e)
        return [], []

    finally:
        conn.close()
