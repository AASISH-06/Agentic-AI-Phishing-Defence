# 🛡️ Agentic AI Phishing Defence System

[![GitHub License](https://img.shields.io/github/license/AASISH-06/Agentic-AI-Phishing-Defence?style=flat-square)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green?style=flat-square)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/status-active-success?style=flat-square)](https://github.com/AASISH-06/Agentic-AI-Phishing-Defence)

An **automated, AI-powered phishing detection system** that actively monitors Gmail and WhatsApp/SMS for phishing threats. Uses machine learning, NLP analysis, OCR detection, and steganography analysis to identify and alert users about suspicious messages in real-time.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Gmail API Setup](#gmail-api-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Instructions](#usage-instructions)
- [API Endpoints](#api-endpoints)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)
- [License](#license)

---

## 🎯 Project Overview

The **Agentic AI Phishing Defence System** is an automated security solution that provides **24/7 protection** against phishing attacks across multiple communication channels:

- **📧 Gmail**: Automatically scans incoming emails every 60 seconds
- **💬 WhatsApp**: Analyzes incoming messages and alerts users
- **📱 SMS**: Detects phishing attempts in text messages

The system combines **multiple detection techniques**:
- 🤖 Machine Learning (NLP-based classification)
- 🔍 Keyword Pattern Recognition (OCR)
- 🖼️ Steganography Detection (hidden message extraction)
- 📊 Risk Scoring Algorithm

**Real-time Dashboard** displays all scans with risk scores, sender information, and detection timestamps.

---

## ✨ Features

### 🔐 Multi-Channel Monitoring
- ✅ **Gmail Integration**: OAuth-based automatic email scanning
- ✅ **WhatsApp Integration**: Real-time message analysis via Twilio
- ✅ **SMS Detection**: Phishing detection for text messages
- ✅ **Automated Alerts**: WhatsApp/SMS alerts for high-risk messages

### 🧠 Advanced Detection Techniques
- ✅ **NLP Phishing Classifier**: ML model trained to identify phishing patterns
- ✅ **Keyword Detection**: Scans for 13+ phishing-related keywords
- ✅ **OCR Analysis**: Extracts text from images to detect hidden threats
- ✅ **Steganography Detection**: Identifies hidden messages in images
- ✅ **Risk Scoring**: Composite risk score (0-100) from multiple factors

### 📊 Dashboard & Logging
- ✅ **Real-time Dashboard**: Beautiful UI showing all scans with risk levels
- ✅ **Database Logging**: SQLite storage of all scan results
- ✅ **Email History**: Complete Gmail scan logs with timestamps
- ✅ **Message History**: WhatsApp/SMS message archive

### 🔧 User-Friendly
- ✅ **Web Interface**: Access dashboard at `http://localhost:5000`
- ✅ **Easy Setup**: Simple configuration with environment variables
- ✅ **Zero Configuration**: Works out-of-the-box with example files
- ✅ **Automatic Updates**: Runs on schedule without manual intervention

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WEB INTERFACE                            │
│            (Flask Backend + HTML Dashboard)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  BACKGROUND SCHEDULER                       │
│           (APScheduler - Runs every 60 seconds)            │
└─────────────────────────────────────────────────────────────┘
              │                           │
              ↓                           ↓
      ┌──────────────┐          ┌──────────────┐
      │ Gmail Module │          │ Twilio Module│
      │  (Gmail API) │          │   (Webhook)  │
      └──────────────┘          └──────────────┘
              │                           │
              ↓                           ↓
      ┌──────────────────────────────────────┐
      │    ANALYZER ENGINE                   │
      │  ┌────────────────────────────────┐ │
      │  │ NLP Phishing Classifier (ML)   │ │
      │  │ Keyword Detection (OCR)        │ │
      │  │ Steganography Detection        │ │
      │  │ Risk Score Calculation         │ │
      │  └────────────────────────────────┘ │
      └──────────────────────────────────────┘
              │
              ↓
      ┌──────────────────────────────────────┐
      │    ALERT SYSTEM                      │
      │  • WhatsApp Notifications            │
      │  • SMS Alerts                        │
      │  • Move to Spam (Gmail)              │
      └──────────────────────────────────────┘
              │
              ↓
      ┌──────────────────────────────────────┐
      │    DATABASE (SQLite)                 │
      │  • Scan Logs                         │
      │  • Email History                     │
      │  • Message Archive                   │
      └──────────────────────────────────────┘
```

---

## 💻 Tech Stack

### Backend
- **Framework**: Flask 3.0+ (Python Web Framework)
- **Scheduling**: APScheduler (Background Tasks)
- **Database**: SQLite3 (Persistent Storage)
- **ML/NLP**: scikit-learn, NLTK
- **Image Processing**: PIL/Pillow, pytesseract (OCR)

### APIs & Integrations
- **Gmail API**: Google OAuth 2.0 for email access
- **Twilio API**: WhatsApp & SMS messaging
- **Google Cloud**: OAuth credentials

### Frontend
- **HTML5 + CSS3**: Responsive dashboard UI
- **Real-time Updates**: JavaScript polling (auto-refresh)
- **Styling**: Modern gradient design with animations

### DevOps
- **Git**: Version control
- **GitHub**: Repository hosting
- **Environment Management**: python-dotenv

### Libraries & Dependencies
```
Flask==3.0+
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
twilio
scikit-learn
pillow
pytesseract
apscheduler
python-dotenv
```

---

## 📁 Project Structure

```
Agentic-AI-Phishing-Defence/
│
├── 📄 README.md                      # Project documentation
├── 📄 requirements.txt               # Python dependencies
├── 🔒 .gitignore                     # Git ignore rules
├── 📋 .env.example                   # Environment variables template
│
├── 📁 models/                        # ML Models
│   ├── model.joblib                  # Phishing classifier (trained)
│   └── vectorizer.joblib             # TF-IDF vectorizer
│
├── 📁 src/                           # Source code
│   ├── app.py                        # Flask application & routes
│   ├── analyzer.py                   # Phishing detection engine
│   ├── worker.py                     # Background scheduler & Gmail scanner
│   ├── gmail_utils.py                # Gmail API integration
│   ├── twilio_utils.py               # WhatsApp/SMS alerts
│   ├── ocr_utils.py                  # OCR text extraction
│   ├── stego.py                      # Steganography detection
│   ├── logger_db.py                  # Database operations
│   ├── retrain.py                    # Model retraining script
│   │
│   ├── credentials.example.json      # Google OAuth template
│   ├── config.example.py             # Configuration template
│   ├── config.py                     # Configuration (ignored in git)
│   │
│   ├── 📁 data/
│   │   └── scans.db                  # SQLite database (logs)
│   │
│   └── 📁 templates/
│       ├── index.html                # Landing page
│       └── dashboard.html            # Real-time dashboard
│
└── 📁 .git/                          # Git repository

Key Ignored Files (Not in GitHub):
  • token.json                        # Gmail OAuth token (personal)
  • credentials.json                  # OAuth keys (sensitive)
  • config.py                         # API keys (sensitive)
  • .env                              # Environment variables (sensitive)
```

---

## 🚀 Installation

### Prerequisites
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ Git
- ✅ Virtual environment (recommended)
- ✅ Tesseract OCR (for image text extraction)

### Step 1: Clone the Repository

```bash
git clone https://github.com/AASISH-06/Agentic-AI-Phishing-Defence.git
cd Agentic-AI-Phishing-Defence
```

### Step 2: Create Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Tesseract OCR

**Windows:**
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add to `ocr_utils.py`:
```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

### Step 5: Configure Environment Variables

```bash
# Copy example files
cp .env.example .env
cp credentials.example.json credentials.json
cp src/config.example.py src/config.py
```

Edit `.env` with your credentials (see next sections).

---

## 🔐 Gmail API Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"** → Enter name → Click **Create**
3. Wait for project to be created

### Step 2: Enable Gmail API

1. In the console, go to **APIs & Services** → **Library**
2. Search for **"Gmail API"**
3. Click on it → Click **Enable**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ Create Credentials"** → Select **"OAuth Client ID"**
3. If prompted, configure OAuth consent screen:
   - User type: **External**
   - Add required scopes:
     - `https://www.googleapis.com/auth/gmail.modify`
     - `https://www.googleapis.com/auth/userinfo.email`
4. Application type: **Desktop application**
5. Click **Create**
6. Download the JSON file → Rename to `credentials.json`
7. Place it in the project root or `src/` folder

### Step 4: Test Gmail Connection

```bash
python src/app.py
```

First run will open a browser asking you to authorize. Complete the authorization.
A `token.json` file will be created automatically.

---

## ⚙️ Configuration

### Update `.env` File

```env
# Gmail Configuration
GMAIL_CREDENTIALS=credentials.json
GMAIL_TOKEN_PATH=token.json

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_NUMBER=whatsapp:+1234567890
ALERT_PHONE=whatsapp:+91XXXXXXXXXX

# Poll Interval
POLL_INTERVAL_SECONDS=60

# Risk Threshold
RISK_THRESHOLD=50
```

### Update `src/config.py` File

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
ALERT_PHONE = os.getenv("ALERT_PHONE")

# Gmail
GMAIL_CREDENTIALS = os.getenv("GMAIL_CREDENTIALS", "credentials.json")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN_PATH", "token.json")

# Settings
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
RISK_THRESHOLD = int(os.getenv("RISK_THRESHOLD", "50"))
```

---

## ▶️ Running the Application

### Start the Flask Backend

```bash
# Make sure virtual environment is activated
python src/app.py
```

**Expected Output:**
```
🕒 Starting Agentic AI Phishing Defense every 60s...
✅ Background worker started successfully.
 * Running on http://127.0.0.1:5000
```

### Access the Dashboard

Open your browser and go to:
```
http://localhost:5000
```

You should see:
- **Home Page** (`/`) - Welcome screen
- **Dashboard** (`/dashboard`) - Real-time scan logs
- **Twilio Webhook** (`/twilio/incoming`) - Test WhatsApp messages

---

## 📖 Usage Instructions

### Automatic Gmail Scanning

The system automatically scans Gmail every **60 seconds**:

1. ✅ Fetches unread emails from Gmail
2. ✅ Analyzes each email for phishing indicators
3. ✅ Generates risk score (0-100)
4. ✅ Logs results in dashboard
5. ✅ Sends WhatsApp alert if risk ≥ 50
6. ✅ Moves high-risk emails to SPAM

### Test WhatsApp Messages

**Via Dashboard:**
1. Go to `http://localhost:5000/twilio/incoming`
2. Fill in the form:
   - From: `whatsapp:+919441410301`
   - Body: `"Your bank account is locked. Verify here: http://secure-login.net"`
3. Click **"Send Test POST"**
4. Check dashboard for the result

**Via Twilio Webhook:**
Send a real WhatsApp message to your Twilio Sandbox number, the app will:
1. Receive message via webhook
2. Analyze for phishing
3. Display in dashboard
4. Send alert if risky

### View Scan Results

**Dashboard Features:**
- 📊 **Gmail Logs**: All scanned emails with risk scores
- 💬 **WhatsApp Logs**: Incoming messages and analysis
- ⏰ **Timestamps**: Exact time of each scan
- 📈 **Risk Scores**: Color-coded (Green: Safe, Yellow: Medium, Red: Phishing)

---

## 🔌 API Endpoints

### Web Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/dashboard` | GET | Real-time dashboard |
| `/twilio/incoming` | GET/POST | Twilio webhook endpoint |
| `/_status_quick` | GET | Health check |

### Example Requests

**Test Phishing Detection:**
```bash
curl -X POST http://localhost:5000/twilio/incoming \
  -d "From=whatsapp%3A%2B919441410301" \
  -d "Body=Your+bank+account+is+locked.+Verify+here%3A+http%3A%2F%2Fsecure-login.net"
```

---

## 🎯 How Phishing Detection Works

### Risk Score Calculation

```
Risk Score = (0.6 × NLP_Score × 100) + (0.25 × OCR_Contribution) + (0.15 × Stego_Contribution)

Where:
• NLP_Score: ML model confidence (0.0-1.0)
• OCR_Contribution: 60 if keywords found, else 0
• Stego_Contribution: 100 if hidden text detected, else 0
```

### Example Analysis

**Email:** "Your bank account is locked. Verify here: http://secure-login.net"

```
1. NLP Analysis:
   - Model confidence: 0.75 (high phishing probability)
   - Contribution: 0.6 × 75 = 45

2. OCR Keyword Detection:
   - Found: ["bank", "account", "verify", "locked"]
   - Contribution: 0.25 × 60 = 15

3. Steganography Detection:
   - No hidden images
   - Contribution: 0.15 × 0 = 0

4. Final Risk Score: 45 + 15 + 0 = 60/100 ⚠️ PHISHING ALERT
```

---

## 🚀 Future Enhancements

- [ ] **Machine Learning Model Improvements**
  - [ ] Train on larger phishing dataset
  - [ ] Add deep learning (LSTM/Transformer) models
  - [ ] Implement active learning from user feedback

- [ ] **Advanced Detection**
  - [ ] URL reputation checking (VirusTotal API)
  - [ ] Sender authentication (SPF/DKIM/DMARC)
  - [ ] Attachment malware scanning
  - [ ] Email header analysis

- [ ] **Multi-Platform Support**
  - [ ] Telegram bot integration
  - [ ] Slack integration
  - [ ] Microsoft Outlook support
  - [ ] Discord notifications

- [ ] **User Management**
  - [ ] Multi-user support with login
  - [ ] User-specific whitelists/blacklists
  - [ ] Email subscription management
  - [ ] Admin dashboard

- [ ] **Enhanced Dashboard**
  - [ ] Real-time alerts with WebSocket
  - [ ] Export scan reports (PDF/CSV)
  - [ ] Advanced filtering and search
  - [ ] Analytics & statistics

- [ ] **Deployment**
  - [ ] Docker containerization
  - [ ] Cloud deployment (AWS, GCP, Azure)
  - [ ] Kubernetes orchestration
  - [ ] CI/CD pipeline with GitHub Actions

- [ ] **API Development**
  - [ ] RESTful API with rate limiting
  - [ ] API documentation (Swagger/OpenAPI)
  - [ ] Third-party integrations

---

## 👥 Contributors

- **AASISH-06** - Project Creator & Developer
  - GitHub: [@AASISH-06](https://github.com/AASISH-06)
  - Email: aasishlebaka74@gmail.com

### Contributing

We welcome contributions! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/YourFeature`)
3. **Commit** your changes (`git commit -m 'Add YourFeature'`)
4. **Push** to the branch (`git push origin feature/YourFeature`)
5. **Open** a Pull Request

Please ensure:
- ✅ Code follows PEP 8 style guide
- ✅ No hardcoded secrets
- ✅ All features are tested
- ✅ Documentation is updated

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Gmail API** - Google Cloud Platform
- **Twilio API** - WhatsApp & SMS integration
- **scikit-learn** - Machine learning library
- **Flask** - Web framework
- **APScheduler** - Background task scheduler

---

## 📞 Support & Contact

- 📧 **Email**: aasishlebaka74@gmail.com
- 🐛 **Issues**: [Report a bug](https://github.com/AASISH-06/Agentic-AI-Phishing-Defence/issues)
- 💡 **Suggestions**: [Request a feature](https://github.com/AASISH-06/Agentic-AI-Phishing-Defence/discussions)
- 💬 **Discussion**: [Join discussions](https://github.com/AASISH-06/Agentic-AI-Phishing-Defence/discussions)

---

## 🎓 Learning Resources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Twilio WhatsApp Documentation](https://www.twilio.com/docs/whatsapp)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn ML Guide](https://scikit-learn.org/stable/)
- [Pytesseract OCR](https://github.com/madmaze/pytesseract)

---

## ⭐ Show Your Support

If you find this project helpful, please give it a **⭐ Star** on GitHub!

```
https://github.com/AASISH-06/Agentic-AI-Phishing-Defence
```

---

**Last Updated**: June 5, 2026  
**Status**: ✅ Active & Maintained  
**Version**: 1.0.0
