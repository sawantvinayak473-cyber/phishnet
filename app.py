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

    if request.method == "POST":
        text = request.form.get("url")

        if text:
            if model:
                pred = model.predict([text])[0]
                prob = model.predict_proba([text])[0][pred]
            else:
                pred = 0 if "login" in text or "verify" in text else 1
                prob = 0.85 if pred == 0 else 0.65

            score = int(prob * 100)
            confidence = round(prob, 2)

            if pred == 1:
                label = "legitimate"
            else:
                label = "phishing"

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