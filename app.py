# app.py - CA Assist Pro (Chat + Voice + Monetization)
import streamlit as st
import streamlit.components.v1 as components
import os
import time
import random

st.set_page_config(
    page_title="CA Assist Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Session State ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_error" not in st.session_state:
    st.session_state.voice_error = ""

# ---------- Custom CSS (Professional) ----------
def get_css(dark):
    if dark:
        return """
        <style>
        body, .stApp { background: #0e1117; color: #f0f0f0; }
        .header { background: linear-gradient(135deg, #0a2f44, #1a5a7a); padding: 1.5rem; border-radius: 16px; color: white; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .chat-user { background: #1e2a3a; padding: 10px 15px; border-radius: 12px; margin: 5px 0; text-align: right; border-right: 3px solid #4ecdc4; }
        .chat-bot { background: #1e1e2f; padding: 10px 15px; border-radius: 12px; margin: 5px 0; border-left: 3px solid #4ecdc4; }
        .step-card { background: #1e1e2f; padding: 1.2rem; border-radius: 12px; margin: 0.8rem 0; border-left: 5px solid #4ecdc4; }
        .link-btn { background: #4ecdc4; color: #0e1117; padding: 0.5rem 1.2rem; border-radius: 25px; text-decoration: none; display: inline-block; font-weight: 600; }
        .donate-btn { background: #ff6b6b; color: white; padding: 0.5rem 1rem; border-radius: 25px; text-align: center; text-decoration: none; display: inline-block; font-weight: 600; }
        </style>
        """
    else:
        return """
        <style>
        .header { background: linear-gradient(135deg, #2c3e50, #3d5a6d); padding: 1.5rem; border-radius: 16px; color: white; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .chat-user { background: #e8f0fe; padding: 10px 15px; border-radius: 12px; margin: 5px 0; text-align: right; border-right: 3px solid #007bff; }
        .chat-bot { background: #f8f9fa; padding: 10px 15px; border-radius: 12px; margin: 5px 0; border-left: 3px solid #28a745; }
        .step-card { background: #f8f9fa; padding: 1.2rem; border-radius: 12px; margin: 0.8rem 0; border-left: 5px solid #28a745; }
        .link-btn { background: #007bff; color: white; padding: 0.5rem 1.2rem; border-radius: 25px; text-decoration: none; display: inline-block; font-weight: 600; }
        .donate-btn { background: #ff6b6b; color: white; padding: 0.5rem 1rem; border-radius: 25px; text-align: center; text-decoration: none; display: inline-block; font-weight: 600; }
        </style>
        """
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ---------- Voice Input (Fixed: no-speech handled) ----------
voice_html = """
<script>
function startVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        document.getElementById('voice-status').innerHTML = '❌ Browser not supported. Please use Chrome/Edge.';
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'hi-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;
    const btn = document.getElementById('voice-btn');
    const status = document.getElementById('voice-status');
    btn.textContent = '🎤 Listening...';
    btn.style.background = '#ff6b6b';
    status.innerHTML = '🎙️ Speak now...';
    recognition.start();
    recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        const inputField = parent.document.querySelector('textarea[data-testid="stTextArea"]');
        if (inputField) {
            inputField.value = spokenText;
            inputField.dispatchEvent(new Event('input', { bubbles: true }));
        }
        // Click send button
        const sendBtn = parent.document.querySelector('button[kind="primary"]');
        if (sendBtn) sendBtn.click();
        btn.textContent = '🎤 Speak';
        btn.style.background = '#007bff';
        status.innerHTML = '✅ Done!';
    };
    recognition.onerror = (event) => {
        let msg = '';
        if (event.error === 'no-speech') {
            msg = '❌ No speech detected. Please type your question below.';
        } else if (event.error === 'audio-capture') {
            msg = '❌ Microphone not found. Please allow microphone permission.';
        } else {
            msg = '❌ Error: ' + event.error + '. Please type your question.';
        }
        status.innerHTML = msg;
        btn.textContent = '🎤 Speak';
        btn.style.background = '#007bff';
    };
    recognition.onend = () => {
        btn.textContent = '🎤 Speak';
        btn.style.background = '#007bff';
    };
}
</script>
<div>
    <button id="voice-btn" onclick="startVoiceInput()" style="background:#007bff; color:white; border:none; border-radius:25px; padding:0.5rem 1.2rem; cursor:pointer; font-size:15px; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
        🎤 Speak
    </button>
    <div id="voice-status" style="margin-top:5px; font-size:14px;"></div>
</div>
"""
components.html(voice_html, height=100)

# ---------- Chatbot Logic ----------
def get_bot_response(user_msg):
    """Smart keyword-based response (no AI, instant)"""
    msg = user_msg.lower().strip()
    
    # GST Registration
    if any(w in msg for w in ["gst registration", "gst register", "how to get gst", "gst number", "new registration"]):
        return f"""
        <strong>📋 GST Registration Guide</strong><br><br>
        <strong>Documents:</strong> PAN, Aadhaar, address proof, bank statement, photo.<br>
        <strong>Steps:</strong><br>
        1. Visit <a href='https://www.gst.gov.in' target='_blank'>GST Portal</a><br>
        2. New Registration → Fill Part A → Get TRN<br>
        3. Complete Part B → Upload docs → Submit<br>
        <strong>Fee:</strong> ₹0<br>
        <a href='https://www.gst.gov.in' target='_blank' class='link-btn'>Start Registration →</a>
        """
    
    # ITR forms
    if any(w in msg for w in ["itr", "income tax return", "which form", "itr form"]):
        return """
        <strong>📝 ITR Forms Guide</strong><br><br>
        <strong>ITR-1 (Sahaj):</strong> Salary + one house property + other sources (≤ ₹50L)<br>
        <strong>ITR-2:</strong> Capital gains / multiple houses / foreign assets<br>
        <strong>ITR-3:</strong> Business or professional income (regular accounting)<br>
        <strong>ITR-4 (Sugam):</strong> Presumptive taxation (44AD/44ADA)<br>
        <a href='https://www.incometax.gov.in' target='_blank' class='link-btn'>File ITR →</a>
        """
    
    # TDS/TCS
    if any(w in msg for w in ["tcs", "amazon", "flipkart", "marketplace", "e-commerce"]):
        return """
        <strong>🏦 TCS on E‑commerce</strong><br><br>
        • Amazon/Flipkart deducts <strong>1% TCS</strong> before payout.<br>
        • Claim by checking GSTR‑2B on 14th of next month.<br>
        <a href='https://services.gst.gov.in/services/login' target='_blank' class='link-btn'>Check TCS Credit →</a>
        """
    
    # Penalty
    if any(w in msg for w in ["penalty", "late fee", "interest", "late filing"]):
        return """
        <strong>⚠️ Late Fee & Penalty</strong><br><br>
        • GSTR‑3B (with tax): ₹50/day (₹25 CGST + ₹25 SGST)<br>
        • Nil return: ₹20/day<br>
        • Interest: 18% per annum on tax due<br>
        <a href='https://www.gst.gov.in' target='_blank' class='link-btn'>File Pending Returns →</a>
        """
    
    # Default fallback
    return """
    🤖 I can help with:<br>
    • GST Registration<br>
    • ITR Forms (which one to use)<br>
    • TCS on Amazon/Flipkart<br>
    • Late fee / Penalty<br>
    • e‑Way Bill<br>
    • MSME Registration<br><br>
    <strong>Ask me anything about these topics!</strong>
    """

# ---------- Chat Interface ----------
st.markdown('<div class="header"><h1>🚀 CA Assist Pro</h1><p>Your Virtual CA – Chat, Voice, and Guides</p></div>', unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-user"><strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot"><strong>🤖 CA Assist:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

# Input area
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area("Ask your question", placeholder="e.g., How to register for GST?", key="chat_input", label_visibility="collapsed", height=80)
    with col2:
        send_btn = st.button("Send 📤", use_container_width=True)

if send_btn and user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # Get bot response
    bot_reply = get_bot_response(user_input)
    st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
    st.rerun()

# Quick questions row
st.markdown("**💡 Quick Questions:**")
cols = st.columns(4)
quick_qs = ["GST registration", "Which ITR form?", "TCS on Amazon", "Late fee penalty"]
for i, q in enumerate(quick_qs):
    if cols[i].button(q, use_container_width=True):
        st.session_state.chat_history.append({"role": "user", "content": q})
        bot_reply = get_bot_response(q)
        st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
        st.rerun()

# ---------- Sidebar: Mascot + Dark Mode + Monetization ----------
with st.sidebar:
    # Mascot with fallback
    mascot_files = ["1387.png", "Your_CA_TAX_FORM_assist.webp", "1702_5044002421411143846.webp"]
    mascot_loaded = False
    for f in mascot_files:
        if os.path.exists(f):
            st.image(f, width=180, caption="🤵 CA Assist")
            mascot_loaded = True
            break
    if not mascot_loaded:
        st.markdown("### 🤵 CA Assist")
        st.info("Add a mascot image (1387.png) to personalize.")
    
    # Dark Mode
    dark_toggle = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_toggle
        st.rerun()
    
    st.markdown("---")
    # Monetization Section
    st.markdown("### 💰 Support CA Assist")
    st.markdown("Help us keep this free for everyone!")
    st.markdown("""
    <a href="https://buy.stripe.com/your-link" target="_blank" class="donate-btn">☕ Buy a Coffee</a>
    <br><br>
    <strong>Pro Features (coming soon):</strong>
    <br>• PDF Export of guides
    <br>• Unlimited voice queries
    <br>• Priority support
    <br><span style="font-size:12px;">₹199/year</span>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📌 Quick Links")
    st.markdown("""
    - [GST Portal](https://www.gst.gov.in)
    - [Income Tax](https://www.incometax.gov.in)
    - [e-Way Bill](https://ewaybillgst.gov.in)
    - [MSME Registration](https://udyamregistration.gov.in)
    """)

# ---------- Footer ----------
st.markdown("---")
st.caption("🚀 **CA Assist Pro** – Made with ❤️ for Indian taxpayers | Free forever (with optional support)")
