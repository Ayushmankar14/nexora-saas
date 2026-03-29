import streamlit as st
from db import create_user, login_user
import time
from streamlit_cookies_manager import EncryptedCookieManager

# 🔐 PAGE CONFIG (TOP PE)
st.set_page_config(page_title="Nexora SaaS", layout="centered")

# 🍪 COOKIES SETUP
cookies = EncryptedCookieManager(password="super-secret-key")

if not cookies.ready():
    st.stop()

# 🧠 SESSION INIT
if "user" not in st.session_state:
    st.session_state.user = None

# 🔄 AUTO LOGIN FROM COOKIES
if st.session_state.user is None:
    if "user_id" in cookies and "role" in cookies:
        user_id = int(cookies["user_id"])
        role = cookies["role"]

        # basic user tuple (safe fallback)
        st.session_state.user = (user_id, "", "", role, 0)

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

# 🧠 INTRO (IMPORTANT FOR RAZORPAY)
st.markdown("""
### 🚀 Nexora SaaS

A simple tool for sellers to manage products and orders.

💰 Subscription: ₹199/month  
📦 Customers pay sellers directly (UPI/COD)
""")

# 🏷️ HEADER
st.markdown("<h1 style='text-align:center; color:#facc15;'>📦 Nexora SaaS</h1>", unsafe_allow_html=True)

# 🔁 IF ALREADY LOGGED IN → REDIRECT
if st.session_state.user:
    role = st.session_state.user[3]

    if role == "Seller":
        st.switch_page("pages/seller.py")
    else:
        st.switch_page("pages/customer.py")

# 🔘 MENU
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

            # 🍪 SAVE IN COOKIES
            cookies["user_id"] = str(user[0])
            cookies["role"] = user[3]
            cookies.save()

            if user[3] == "Seller":
                st.switch_page("pages/seller.py")
            else:
                st.switch_page("pages/customer.py")
        else:
            st.error("Invalid credentials")
