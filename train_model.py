import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = {
    "url": [
        "paypal.com",
        "google.com",
        "github.com",
        "amazon.com",
        "bankofamerica.com",
        "login-paypal-alert.com",
        "verify-account-paypal.net",
        "secure-update-bank.xyz",
        "free-money-win.click",
        "apple-id-confirm.ru",
        "facebook-login-security.com",
        "netflix-update-billing.info",
        "bank-verification-free.xyz",
        "signin-ebay-alert.com"
    ],
    "label": [
        0,0,0,0,0,
        1,1,1,1,1,1,1,1,1
    ]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["url"])
y = df["label"]

model = LogisticRegression()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model and vectorizer saved!")