import streamlit as st
from db import add_product, get_products, delete_product

# SESSION
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

user = st.session_state.user
seller_id = user[0]
is_paid = user[4]

# LOGOUT
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.switch_page("app.py")

st.title("📦 Manage Products")

products = get_products()

# 🔒 FREE LIMIT
if not is_paid and len(products) >= 5:
    st.warning("Free plan limit reached (5 products)")
    if st.button("🚀 Upgrade"):
        st.switch_page("pages/subscribe.py")
    st.stop()

# ADD PRODUCT
name = st.text_input("Product Name")
price = st.number_input("Price", min_value=10, value=50)

if st.button("➕ Add Product"):
    add_product(seller_id, name, price)
    st.success("Added!")

st.divider()

# SHOW PRODUCTS
for p in products:
    if p[1] != seller_id:
        continue

    col1, col2, col3 = st.columns([3,2,1])

    col1.write(f"**{p[2]}**")
    col2.write(f"₹{p[3]}")

    if col3.button("❌", key=f"del_{p[0]}"):
        delete_product(p[0])
        st.rerun()