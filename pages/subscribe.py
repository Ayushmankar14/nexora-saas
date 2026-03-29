import streamlit as st
from db import activate_subscription

# SESSION
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")
    st.stop()

user_id = st.session_state.user[0]

st.markdown("""
<h1 style='text-align:center; color:#22c55e;'>🚀 Upgrade to Pro</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background:#052e16; padding:30px; border-radius:15px;'>

<h2 style='color:#facc15;'>₹199 / month</h2>

✔ Unlimited Products  
✔ Unlimited Orders  
✔ Priority Support  
✔ Future AI Features  

</div>
""", unsafe_allow_html=True)

st.divider()

# 💳 PAYMENT LINK (PUT YOUR RAZORPAY LINK)
PAYMENT_LINK = "https://rzp.io/rzp/1SvDGSwY"

if st.button("💳 Subscribe Now"):
    st.markdown(f"[👉 Pay ₹199]({PAYMENT_LINK})")

# TEST ACTIVATION
if st.button("✅ I have Paid"):
    activate_subscription(user_id)
    st.success("Subscription Activated 🎉")