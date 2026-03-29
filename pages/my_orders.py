import streamlit as st
import pandas as pd
from db import get_orders_customer

# SESSION
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

customer_id = st.session_state.user[0]

st.title("📦 My Orders")

orders = get_orders_customer(customer_id)

if not orders:
    st.info("No orders yet")
    st.stop()

df = pd.DataFrame(orders, columns=[
    "id","seller_id","customer_id","product","price","qty","total","status"
])

for _, row in df.iterrows():

    if row["status"] == "Pending":
        status = "🟡 Pending"
    elif row["status"] == "Shipped":
        status = "🔵 Shipped"
    else:
        status = "🟢 Delivered"

    st.markdown(f"""
    **{row['product']}** x{row['qty']}  
    ₹{row['total']}  
    Status: {status}
    """)

    st.divider()