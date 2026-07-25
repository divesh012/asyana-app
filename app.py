from flask import Flask, render_template, jsonify, request
import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise Exception("Razorpay keys not found in .env")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.route("/")
def home():
    return render_template("index.html", key_id=RAZORPAY_KEY_ID)

@app.route("/scholarship")
def scholarship():
    return render_template("scholarship.html")

@app.route("/old-age")
def old_age():
    return render_template("old_age.html")

@app.route("/aasanya_bhavan")
def aasanya_bhavan():
    return render_template("aasanyaBhavan.html")

#------Payment Page -------------#

@app.route("/create-order")
def create_order():
    try:
        order = client.order.create({
            "amount": 1000,      # ₹10
            "currency": "INR",
            "payment_capture": 1
        })

        return jsonify({
            "success": True,
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/payment-success", methods=["POST"])
def payment_success():

    data = request.get_json()

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        return jsonify({
            "success": True,
            "message": "Payment Verified"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
