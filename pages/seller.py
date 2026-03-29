import streamlit as st
import pandas as pd
from db import get_orders_seller

# SESSION
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

user = st.session_state.user
seller_id = user[0]
is_paid = user[4]

# 🚪 LOGOUT
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.switch_page("app.py")

st.title("📊 Seller Dashboard")

# 🔒 LOCK SYSTEM
if not is_paid:
    st.warning("🔒 You are on FREE plan (limit: 5 products)")

    if st.button("🚀 Upgrade Now"):
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