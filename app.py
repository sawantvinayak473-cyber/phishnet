from email.mime import text

from flask import Flask, render_template, request
import os
import pickle

app = Flask(__name__)

model = None
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except:
    pass


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = 0
    confidence = 0
    label = ""
    text = ""

    if request.method == "POST":
        text = request.form.get("url")

    result = False
    score = 0
    confidence = 0
    label = ""

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
        elif score > 30:
            label = "Suspicious"
        else:
            label = "Legitimate"

        result = True

    return render_template(
        "index.html",
        result=result,
        score=score,
        confidence=confidence,
        label=label
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)