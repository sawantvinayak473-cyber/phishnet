<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

app = Flask(__name__)

data = {
    "text": [
        "Your account has been suspended click here",
        "Verify your bank login immediately",
        "Urgent action required reset password now",
        "Meeting scheduled tomorrow at 10am",
        "Project deadline extended",
        "Lunch at 2pm?",
        "Security alert unusual login detected",
        "Invoice attached for your review"
    ],
    "label": [1, 1, 1, 0, 0, 0, 1, 0]
}

df = pd.DataFrame(data)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

df["text"] = df["text"].apply(clean_text)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(df["text"], df["label"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    text = data.get("text", "")
    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]
    probability = model.predict_proba([cleaned])[0][prediction]

    return jsonify({
        "prediction": int(prediction),
        "confidence": float(probability)
    })

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

=======
from flask import Flask, render_template, request, jsonify
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

app = Flask(__name__)

data = {
    "text": [
        "Your account has been suspended click here",
        "Verify your bank login immediately",
        "Urgent action required reset password now",
        "Meeting scheduled tomorrow at 10am",
        "Project deadline extended",
        "Lunch at 2pm?",
        "Security alert unusual login detected",
        "Invoice attached for your review"
    ],
    "label": [1, 1, 1, 0, 0, 0, 1, 0]
}

df = pd.DataFrame(data)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

df["text"] = df["text"].apply(clean_text)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

model.fit(df["text"], df["label"])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    text = data.get("text", "")
    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]
    probability = model.predict_proba([cleaned])[0][prediction]

    return jsonify({
        "prediction": int(prediction),
        "confidence": float(probability)
    })

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 356acd049ea2f22d119ffb982b647351fa584b32
