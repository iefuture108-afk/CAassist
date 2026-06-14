import streamlit as st

st.set_page_config(page_title="CA Teacher", page_icon="👨‍🏫", layout="wide")

st.markdown("""
<style>
.teacher-header {
    background: #2c3e50;
    padding: 1rem;
    border-radius: 12px;
    color: white;
    text-align: center;
}
.step-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 5px solid #28a745;
}
.link-btn {
    background: #007bff;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    text-decoration: none;
    display: inline-block;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Helper functions (Hinglish) ----------
def show_gst_registration():
    st.markdown("### 📋 GST Registration – Step by Step (E‑commerce seller ke liye)")
    st.markdown("""
    <div class="step-card">
    ✅ <strong>Step 1:</strong> Apna PAN card ready rakhein (personal PAN bhi chalega).<br>
    ✅ <strong>Step 2:</strong> Address proof rakhein (bijli bill / rent agreement).<br>
    ✅ <strong>Step 3:</strong> Bank statement ya cancelled cheque rakhein.<br>
    ✅ <strong>Step 4:</strong> Neeche diye link pe click karein → New Registration → Part A bharein (PAN, mobile, email).<br>
    ✅ <strong>Step 5:</strong> Jo TRN number mile, use likh kar rakhein.<br>
    ✅ <strong>Step 6:</strong> TRN se login karein → Part B bharein (business details).<br>
    ✅ <strong>Step 7:</strong> Documents upload karein → Submit karein → ARN milega.<br>
    ✅ <strong>Step 8:</strong> 7 din mein aapka GSTIN aa jayega.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="https://www.gst.gov.in" target="_blank" class="link-btn">🔗 GST Portal Open Karein →</a>', unsafe_allow_html=True)

def show_itr_guide():
    st.markdown("### 📝 Kaunsa ITR Form Bharo?")
    opt = st.radio("Apni income ka type chune:", [
        "Salary + ek ghar ka rent + interest (business nahi)",
        "Share market / multiple ghar / foreign assets",
        "Business ya professional income (normal accounting)",
        "Chhoti business (presumptive tax 44AD/44ADA)"
    ])
    if "Salary" in opt:
        st.success("✅ Aapko **ITR-1 (Sahaj)** bharna hai – sabse easy.")
    elif "Share market" in opt:
        st.success("✅ Aapko **ITR-2** bharna hai.")
    elif "Business ya professional" in opt and "presumptive" not in opt:
        st.success("✅ Aapko **ITR-3** bharna hai.")
    else:
        st.success("✅ Aapko **ITR-4 (Sugam)** bharna hai.")
    st.markdown(f'<a href="https://www.incometax.gov.in" target="_blank" class="link-btn">🔗 ITR File Karein →</a>', unsafe_allow_html=True)
    st.caption("📅 Due date: 31 July (audit nahi) | 31 October (audit hai)")

def show_penalty_calculator():
    st.markdown("### ⚠️ Late Fee & Penalty Calculator")
    tax_due = st.number_input("Jo tax aapne nahi bhara (₹)", min_value=0, value=5000)
    days = st.number_input("Kitne din late ho gaye?", min_value=0, value=15)
    late_fee = days * 50
    interest = tax_due * 0.18 * (days / 365)
    total = late_fee + interest
    st.metric("Late Fee (₹50/day)", f"₹{late_fee:,.0f}")
    st.metric("Interest (18% per year)", f"₹{interest:,.0f}")
    st.metric("Total Penalty", f"₹{total:,.0f}", delta="Jaldi bharein, interest badhta hai")
    st.info("💡 Agar aapki koi bhi sale nahi thi (nil return), toh late fee sirf ₹20/day hai.")

def show_tcs_guide():
    st.markdown("### 🏦 Amazon / Flipkart par TCS (seller ke liye)")
    st.markdown("""
    <div class="step-card">
    ✅ Amazon ya Flipkart aapki payment se <strong>1% TCS</strong> kaat leta hai.<br>
    ✅ Yeh TCS <strong>aapka paisa hai</strong> – aap use claim kar sakte ho.<br>
    ✅ Kaise claim karein:<br>
    &nbsp;&nbsp;1. Agle mahine ki 14th tarikh ko GST portal se <strong>GSTR-2B</strong> download karein.<br>
    &nbsp;&nbsp;2. "TCS Credit" section check karein.<br>
    &nbsp;&nbsp;3. Ye credit apne aap GSTR-3B mein aa jayega.<br>
    ✅ Hamesha marketplace ki report ko GSTR-2B se match karein, tabhi file karein.
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="https://services.gst.gov.in/services/login" target="_blank" class="link-btn">🔗 TCS Credit Check Karein →</a>', unsafe_allow_html=True)

# ---------- Main App ----------
st.markdown('<div class="teacher-header"><h1>👨‍🏫 CA Teacher</h1><p>GST, ITR aur penalty ki aasaan guide (Hindi + English)</p></div>', unsafe_allow_html=True)

# Sidebar – Topics in Hinglish
st.sidebar.title("📚 Aap kya karna chahte ho?")
task = st.sidebar.selectbox("Koi ek kaam chune:", [
    "📋 GST Registration karein",
    "📝 Income Tax Return (ITR) bharein",
    "💰 Late Fee / Penalty calculate karein",
    "🏦 Amazon/Flipkart ka TCS samjhein"
])

if task == "📋 GST Registration karein":
    show_gst_registration()
elif task == "📝 Income Tax Return (ITR) bharein":
    show_itr_guide()
elif task == "💰 Late Fee / Penalty calculate karein":
    show_penalty_calculator()
else:
    show_tcs_guide()

# Footer – Tip
st.markdown("---")
st.caption("👨‍🏫 **Teacher ki salah:** GST ya ITR file karne se pehle saare documents ready rakhein. Koi doubt ho to apne kisi CA dost se pooch lein.")

# Chat for quick questions (Hinglish)
with st.expander("💬 Koi chota sawaal poocho (jaise class mein)"):
    q = st.text_input("Apna sawaal likhein:", placeholder="Jaise: GST ke liye kya documents chahiye?")
    if q:
        if "document" in q.lower() or "document" in q.lower():
            st.info("📄 Documents: PAN card, Aadhaar card, address proof, bank statement / cancelled cheque, photo.")
        elif "due date" in q.lower() or "tarikh" in q.lower():
            st.info("📅 GSTR-3B ki last date 20th of next month. ITR ki last date 31 July (mostly).")
        elif "tcs" in q.lower():
            st.info("🏦 Amazon/Flipkart 1% TCS kaat ta hai. Aap GSTR-2B dekh kar claim kar sakte ho.")
        else:
            st.info("👨‍🏫 Main simple teacher hoon. Bade sawaal ke liye upar diye gaye topics mein se chune.")
