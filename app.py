import streamlit as st
from db import create_user, login_user
import time

# ✅ PAGE CONFIG (TOP PE)
st.set_page_config(page_title="Nexora SaaS", layout="centered")

# ✅ SESSION INIT
if "user" not in st.session_state:
    st.session_state.user = None

# 🎨 CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #052e16);
}
button[kind="primary"] {
    background: linear-gradient(135deg, #facc15, #22c55e);
    color: black;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🧠 INTRO (RAZORPAY KE LIYE IMPORTANT)
st.markdown("""
### 🚀 Nexora SaaS

A simple tool for sellers to manage products and orders.

💰 Subscription: ₹199/month  
📦 Customers pay sellers directly (UPI/COD)
""")

# 🏷️ HEADER
st.markdown("<h1 style='text-align:center; color:#facc15;'>📦 Nexora SaaS</h1>", unsafe_allow_html=True)

menu = st.radio("Select Option", ["Login", "Signup"])

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# ---------------- SIGNUP ----------------
if menu == "Signup":
    role = st.selectbox("Role", ["Seller", "Customer"])

    if st.button("Create Account"):
        with st.spinner("Creating account..."):
            time.sleep(1)

        success, msg = create_user(username, password, role)

        if success:
            st.success("Account created! Now login")
        else:
            st.error(msg)

# ---------------- LOGIN ----------------
if menu == "Login":
    if st.button("Login"):
        with st.spinner("Logging in..."):
            time.sleep(1)

        user = login_user(username, password)

        if user:
            st.session_state.user = user

            if user[3] == "Seller":
                st.switch_page("pages/seller.py")
            else:
                st.switch_page("pages/customer.py")
        else:
            st.error("Invalid credentials")
