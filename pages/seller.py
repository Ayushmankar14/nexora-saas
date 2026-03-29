import streamlit as st
import pandas as pd
from db import get_orders_seller
from streamlit_cookies_manager import EncryptedCookieManager

# 🍪 COOKIES
cookies = EncryptedCookieManager(password="super-secret-key")
if not cookies.ready():
    st.stop()

# 🔐 SESSION CHECK
if "user" not in st.session_state or st.session_state.user is None:
    if "user_id" in cookies and "role" in cookies:
        st.session_state.user = (int(cookies["user_id"]), "", "", cookies["role"], 0)
    else:
        st.switch_page("app.py")
        st.stop()

user = st.session_state.user
seller_id = user[0]
is_paid = user[4] if len(user) > 4 else 0

# 🚪 LOGOUT
if st.sidebar.button("🚪 Logout"):
    cookies.clear()
    st.session_state.user = None
    st.switch_page("app.py")

st.title("📊 Seller Dashboard")

# 🔒 FREE PLAN WARNING
if not is_paid:
    st.warning("🔒 Free plan (limit: 5 products)")
    if st.button("🚀 Upgrade"):
        st.switch_page("pages/subscribe.py")

st.divider()

orders = get_orders_seller(seller_id)

if not orders:
    st.info("No orders yet")
    st.stop()

df = pd.DataFrame(orders, columns=[
    "id","seller_id","customer_id","product","price","qty","total","status"
])

st.markdown(f"## 💰 Revenue: ₹{df['total'].sum()}")

for _, row in df.iterrows():
    st.write(f"{row['product']} x{row['qty']} | ₹{row['total']} | {row['status']}")
