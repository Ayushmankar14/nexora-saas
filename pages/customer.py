import streamlit as st
from db import get_products, save_order
from streamlit_cookies_manager import EncryptedCookieManager

# 🍪 COOKIES
cookies = EncryptedCookieManager(password="super-secret-key")
if not cookies.ready():
    st.stop()

# 🔐 SESSION
if "user" not in st.session_state or st.session_state.user is None:
    if "user_id" in cookies and "role" in cookies:
        st.session_state.user = (int(cookies["user_id"]), "", "", cookies["role"], 0)
    else:
        st.switch_page("app.py")
        st.stop()

customer_id = st.session_state.user[0]

# 🚪 LOGOUT
if st.sidebar.button("🚪 Logout"):
    cookies.clear()
    st.session_state.user = None
    st.switch_page("app.py")

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

payment_mode = st.radio("Payment Method", ["UPI", "Cash on Delivery"])

if payment_mode == "UPI":
    st.info("Pay to seller UPI: seller@upi")

if st.button("Place Order"):
    save_order(customer_id, seller_id, selected, price, qty)
    st.success("Order placed 🎉")
