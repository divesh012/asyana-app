from flask import Flask, render_template, jsonify, request
import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

print("KEY ID =", RAZORPAY_KEY_ID)
print("SECRET =", "Loaded" if RAZORPAY_KEY_SECRET else "Missing")


client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)


@app.route("/")
def home():
    return render_template(
        "index.html",
        key_id=RAZORPAY_KEY_ID
    )


@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        order = client.order.create({
            "amount": 1000,
            "currency": "INR"
        })

        return jsonify({
            "success": True,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/payment-success", methods=["POST"])
def payment_success():
    data = request.json

    payment_id = data.get("razorpay_payment_id")
    order_id = data.get("razorpay_order_id")
    signature = data.get("razorpay_signature")

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

        return jsonify({
            "success": True,
            "message": "Payment verified successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
