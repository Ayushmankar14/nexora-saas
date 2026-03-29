import streamlit as st
from db import add_product, get_products, delete_product
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

user = st.session_state.user
seller_id = user[0]
is_paid = user[4] if len(user) > 4 else 0

# 🚪 LOGOUT
if st.sidebar.button("🚪 Logout"):
    cookies.clear()
    st.session_state.user = None
    st.switch_page("app.py")

st.title("📦 Manage Products")

products = get_products()

# 🔒 FREE LIMIT
if not is_paid and len(products) >= 5:
    st.warning("Free limit reached (5 products)")
    if st.button("🚀 Upgrade"):
        st.switch_page("pages/subscribe.py")
    st.stop()

name = st.text_input("Product Name")
price = st.number_input("Price", min_value=10, value=50)

if st.button("➕ Add Product"):
    add_product(seller_id, name, price)
    st.success("Product added!")

st.divider()

for p in products:
    if p[1] != seller_id:
        continue

    col1, col2, col3 = st.columns([3,2,1])

    col1.write(f"**{p[2]}**")
    col2.write(f"₹{p[3]}")

    if col3.button("❌", key=f"del_{p[0]}"):
        delete_product(p[0])
        st.rerun()
