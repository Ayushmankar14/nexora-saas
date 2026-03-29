import streamlit as st
from db import get_products, save_order

# SESSION
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

# LOGOUT
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.switch_page("app.py")

customer_id = st.session_state.user[0]

st.title("🛒 Place Order")

st.page_link("pages/my_orders.py", label="📦 My Orders")

products = get_products()

if not products:
    st.warning("No products available")
    st.stop()

names = [p[2] for p in products]
selected = st.selectbox("Select Product", names)

product = [p for p in products if p[2] == selected][0]

seller_id = product[1]
price = product[3]

qty = st.number_input("Quantity", min_value=1)

total = price * qty
st.success(f"Total: ₹{total}")

# 💳 PAYMENT OPTIONS
payment_mode = st.radio("Select Payment Method", ["UPI", "Cash on Delivery"])

if payment_mode == "UPI":
    st.info("Pay to seller via UPI: seller@upi")

# PLACE ORDER
if st.button("Place Order"):
    save_order(customer_id, seller_id, selected, price, qty)
    st.success("Order placed successfully 🎉")