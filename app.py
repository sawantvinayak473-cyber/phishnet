from flask import Flask, render_template, request, jsonify
import os
import pickle
import sqlite3
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("scans.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT,
            prediction INTEGER,
            confidence REAL,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

model = None
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except:
    pass

def analyze_input(text):
    indicators = []
    domain = None
    https = False

    if text.startswith("http"):
        parsed = urlparse(text)
        domain = parsed.netloc
        https = parsed.scheme == "https"

        if len(domain) > 25:
            indicators.append("Long suspicious domain")

        if any(x in domain for x in ["login", "verify", "secure", "account"]):
            indicators.append("Credential bait keywords")

        if domain.endswith((".ru", ".xyz", ".tk")):
            indicators.append("High-risk domain TLD")

    phishing_words = [
        "urgent", "verify", "password", "account",
        "suspend", "login", "confirm", "bank",
        "payment", "security", "alert"
    ]

    if any(w in text.lower() for w in phishing_words):
        indicators.append("Phishing language detected")

    return {
        "domain": domain,
        "https": https,
        "indicators": indicators
    }

# -------- FIXED SCAN ROUTE (for JS fetch) --------
@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    text = data.get("url", "")

    score = 0

    phishing_keywords = [
        "login", "verify", "update", "bank",
        "secure", "account", "password",
        "click", "urgent", "limited", "suspend"
    ]

    text_lower = text.lower()
    for word in phishing_keywords:
        if word in text_lower:
            score += 10

    score = min(score, 100)
    confidence = round(score / 100, 2)

    if score > 60:
        prediction = 1
    elif score > 30:
        prediction = 1
    else:
        prediction = 0

    analysis = analyze_input(text)

    # save to DB (same as your logic)
    conn = sqlite3.connect("scans.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO scans (input, prediction, confidence, time) VALUES (?,?,?,?)",
        (
            text,
            int(prediction),
            float(confidence),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )
    conn.commit()
    conn.close()

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "analysis": analysis
    })

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = 0
    confidence = 0
    label = ""
    text = ""
    analysis = {"domain": None, "https": False, "indicators": []}

    if request.method == "POST":
        text = request.form.get("url")

        if text:
            text_lower = text.lower()

            phishing_keywords = [
                "login", "verify", "update", "bank",
                "secure", "account", "password",
                "click", "urgent", "limited", "suspend"
            ]

            for word in phishing_keywords:
                if word in text_lower:
                    score += 10

            score = min(score, 100)
            confidence = round(score / 100, 2)

            if score > 60:
                label = "Phishing"
                prediction = 1
            elif score > 30:
                label = "Suspicious"
                prediction = 1
            else:
                label = "Legitimate"
                prediction = 0

            result = True
            analysis = analyze_input(text)

            conn = sqlite3.connect("scans.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO scans (input, prediction, confidence, time) VALUES (?,?,?,?)",
                (
                    text,
                    int(prediction),
                    float(confidence),
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                )
            )
            conn.commit()
            conn.close()

    return render_template(
        "index.html",
        result=result,
        score=score,
        confidence=confidence,
        label=label,
        analysis=analysis
    )

@app.route("/history")
def history():
    conn = sqlite3.connect("scans.db")
    c = conn.cursor()
    c.execute("SELECT input, prediction, confidence, time FROM scans ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)