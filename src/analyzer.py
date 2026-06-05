# src/analyzer.py
import os, re, joblib
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL_PATH = os.path.join("models", "model.joblib")
VEC_PATH = os.path.join("models", "vectorizer.joblib")

if not os.path.exists(MODEL_PATH) or not os.path.exists(VEC_PATH):
    raise FileNotFoundError("Model/vectorizer missing. Run retrain.py first and ensure models exist.")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

print(f"✅ Model loaded from: {MODEL_PATH}")
print(f"✅ Vectorizer loaded from: {VEC_PATH}")
print(f"✅ Model type: {type(model).__name__}")
print(f"✅ Vectorizer vocabulary size: {len(vectorizer.vocabulary_)}")

PHISHING_KEYWORDS = [
    "verify", "account", "password", "suspended", "click here", "urgent",
    "update", "bank", "confirm", "security", "payment", "login", "billing"
]

def clean_text(text):
    if text is None:
        return ""
    t = str(text).lower()
    t = re.sub(r"http\S+", " ", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def nlp_predict(text):
    t = clean_text(text)
    X = vectorizer.transform([t])
    prob = float(model.predict_proba(X)[0][1])
    label = int(prob >= 0.5)
    print(f"   📊 NLP Model - Cleaned text: '{t[:60]}...'")
    print(f"   📊 NLP Model - Probability: {prob:.4f}")
    return prob, label

def ocr_keyword_flag(text):
    t = clean_text(text)
    found = [kw for kw in PHISHING_KEYWORDS if kw in t]
    print(f"   🔎 Keywords - Cleaned text: '{t[:60]}...'")
    print(f"   🔎 Keywords - Found: {found}")
    return (len(found) > 0), found

def compute_risk_score(nlp_score, ocr_flag, stego_flag,
                       w_nlp=0.6, w_ocr=0.25, w_stego=0.15):
    # normalize nlp (0..1) -> scale *100
    nlp_contrib = nlp_score * 100
    ocr_contrib = 60 if ocr_flag else 0
    stego_contrib = 100 if stego_flag else 0
    raw = w_nlp * nlp_contrib + w_ocr * ocr_contrib + w_stego * stego_contrib
    final = max(0, min(100, raw))
    
    # Debug: show calculation
    print(f"   💯 Risk Calculation: ({w_nlp}×{nlp_contrib:.1f}) + ({w_ocr}×{ocr_contrib}) + ({w_stego}×{stego_contrib}) = {raw:.2f} → {final:.2f}")
    
    return final

# =============================
# Unified analysis entry point
# =============================
def analyze_text(message: str):
    """
    Combine NLP phishing prediction, OCR keyword flag, and risk scoring
    into one clean analysis pipeline.
    Returns a dictionary with NLP score, OCR detection flag, and risk_score.
    """
    try:
        # Step 1: NLP phishing model (returns tuple: prob, label)
        nlp_prob, nlp_label = nlp_predict(message)

        # Step 2: OCR keyword detection (returns tuple: flag, keywords_found)
        ocr_flag, ocr_found = ocr_keyword_flag(message)

        # Step 3: Steganography flag (default False for text-only analysis)
        stego_flag = False

        # Step 4: Compute total phishing risk
        risk_score = compute_risk_score(nlp_prob, ocr_flag, stego_flag)
        
        # Debug logging
        print(f"\n🔍 Analysis Details:")
        print(f"   NLP Probability: {nlp_prob:.4f} | Label: {nlp_label}")
        print(f"   OCR Keywords Found: {ocr_flag} | Keywords: {ocr_found}")
        print(f"   Stego Detected: {stego_flag}")
        print(f"   Final Risk Score: {risk_score:.2f}")
        print()

        return {
            "nlp_score": nlp_prob,
            "ocr_detected": ocr_flag,
            "risk_score": risk_score
        }

    except Exception as e:
        print(f"⚠️ Error in analyze_text: {e}")
        import traceback
        traceback.print_exc()
        return {"nlp_score": 0, "ocr_detected": False, "risk_score": 0.0}
