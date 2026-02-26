from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Dummy model (stable demo)
def predict_url(url):
    if not url or len(url.strip()) == 0:
        return 0, 0.0
    
    # simple rule demo
    phishing_keywords = ["login", "verify", "bank", "paypal", "update", "secure"]
    
    score = sum(1 for k in phishing_keywords if k in url.lower())
    
    if score >= 2:
        return 1, round(0.7 + score * 0.05, 2)
    else:
        return 0, round(0.4 + score * 0.05, 2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.get_json()
        url = data.get("url", "")

        pred, conf = predict_url(url)

        return jsonify({
            "prediction": int(pred),
            "confidence": float(conf)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    