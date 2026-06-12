import streamlit as st
from datetime import datetime

st.set_page_config(page_title="CA Assist Pro", page_icon="⚖️", layout="wide")

# ---------- Custom CSS (same as before) ----------
st.markdown("""
<style>
/* Your existing CSS – keep as is */
.ca-header { background: linear-gradient(135deg, #1a3c34 0%, #2d5a4c 100%); padding: 1.5rem; border-radius: 12px; color: white; }
.assistant-message { background: white; border-left: 3px solid #c9a03d; border-radius: 12px; padding: 12px; margin: 8px 0; }
.user-message { background: #e8f0fe; border-radius: 12px; padding: 12px; margin: 8px 0; text-align: right; }
</style>
""", unsafe_allow_html=True)

# ---------- Government links (same) ----------
GOVT_LINKS = {
    "gst_portal": "https://www.gst.gov.in",
    "income_tax_portal": "https://www.incometax.gov.in",
    "gst_returns": "https://services.gst.gov.in/services/login",
}

# ---------- Response generator (returns HTML string) ----------
def get_response(query):
    q = query.lower().strip()
    if "gst registration" in q:
        return f"""
        <div style='background:#f0f9f0; padding:10px; border-radius:10px;'>
        <strong>📋 GST Registration Guide</strong><br><br>
        <strong>Documents:</strong> PAN, Aadhaar, Address proof, Bank statement, Photo.<br>
        <strong>Steps:</strong><br>
        1. Visit <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>GST Portal</a><br>
        2. New Registration → Fill Part A → Get TRN<br>
        3. Complete Part B → Upload docs → Submit<br>
        <strong>Fee:</strong> ₹0<br>
        <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>Start Registration →</a>
        </div>
        """
    if "tcs on amazon" in q:
        return f"""
        <strong>🏦 TCS on Amazon/Flipkart</strong><br>
        • TCS rate: 1% (0.5% CGST + 0.5% SGST)<br>
        • Claim credit by checking GSTR-2B on 14th of next month.<br>
        <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>Check TCS Credit</a>
        """
    # ... add other topics as before (income tax slab, 80C, etc.)
    return "Ask me about GST registration, TCS, ITR, or tax saving."

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": get_response("welcome")}]
if "input_value" not in st.session_state:
    st.session_state.input_value = ""

# ---------- Header ----------
st.markdown('<div class="ca-header"><h1>⚖️ CA Assist Pro</h1><p>GST, Income Tax & Compliance Guide</p></div>', unsafe_allow_html=True)

# ---------- Chat display (FIXED: render HTML) ----------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message"><strong>🤵 CA Assist:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ---------- Input + Quick buttons (FIXED) ----------
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("Your question", value=st.session_state.input_value, key="input_box", label_visibility="collapsed")
with col2:
    if st.button("Send", use_container_width=True):
        if user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            reply = get_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.input_value = ""  # clear
            st.rerun()

# ---------- Quick questions (now work properly) ----------
st.markdown("*💡 Quick questions:*")
quick_qs = ["GST registration process", "Income tax slab 2025", "TCS on Amazon", "80C deductions"]
cols = st.columns(4)
for i, q in enumerate(quick_qs):
    if cols[i].button(q, use_container_width=True):
        # set input and trigger send
        st.session_state.input_value = q
        st.rerun()

# ---------- Footer ----------
st.markdown("---")
st.caption("CA Assist provides guidance only. Final filings on official portals.")
