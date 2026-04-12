from flask import Flask, render_template, jsonify
import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load keys from .env
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.route("/")
def home():
    return render_template("index.html", key_id=RAZORPAY_KEY_ID)


@app.route("/create-order", methods=["GET"])
def create_order():
    order_data = {
        "amount": 1000,  # ₹10 (in paise)
        "currency": "INR",
        "payment_capture": 1
    }
    order = client.order.create(data=order_data)
    return jsonify(order)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
