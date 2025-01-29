from flask import Flask, render_template, request, jsonify
import razorpay

app = Flask(__name__)

# Razorpay API Keys (Replace with your own)
RAZORPAY_KEY_ID = "your_razorpay_key_id"
RAZORPAY_KEY_SECRET = "your_razorpay_key_secret"
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    amount = data.get("amount") * 100  # Convert to paisa
    
    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })
    
    return jsonify(order)

@app.route('/payment_success', methods=['POST'])
def payment_success():
    data = request.json
    payment_id = data.get("razorpay_payment_id")
    order_id = data.get("razorpay_order_id")
    signature = data.get("razorpay_signature")
    
    # Verify payment signature
    try:
        razorpay_client.utility.verify_payment_signature(data)
        return jsonify({"status": "success", "message": "Payment received successfully!"})
    except:
        return jsonify({"status": "failed", "message": "Payment verification failed!"})

if __name__ == '__main__':
    app.run(debug=True)
