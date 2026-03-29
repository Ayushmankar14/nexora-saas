import razorpay

# 🔑 Replace with your keys
client = razorpay.Client(auth=("rzp_test_SX0pkM4Nw1qPmS", "RxQEGnwANhQ6a8uLCi6yBiMP"))

def create_order(amount):
    order = client.order.create({
        "amount": amount * 100,  # paisa
        "currency": "INR",
        "payment_capture": 1
    })
    return order["id"]