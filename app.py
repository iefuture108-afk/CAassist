# app.py - CA Deployer (FIXED: image fallback, voice input, dark mode)
import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="CA Deployer", page_icon="🚀", layout="wide")

# ---------- Dark Mode Toggle ----------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------- CSS (light/dark) ----------
def get_css(dark):
    if dark:
        return """
        <style>
        body, .stApp { background-color: #1e1e2f; color: #f0f0f0; }
        .deployer-header {
            background: #0a2f44;
            padding: 1rem;
            border-radius: 12px;
            color: white;
            text-align: center;
        }
        .step-card {
            background: #2a2a3b;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 5px solid #28a745;
            color: #f0f0f0;
        }
        .stButton > button, .stSelectbox, .stRadio, .stTextInput > div > div > input {
            background-color: #2a2a3b;
            color: #f0f0f0;
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
        """
    else:
        return """
        <style>
        .deployer-header {
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
        """

st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ---------- Voice Input Component (improved) ----------
voice_html = """
<script>
function startVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert("Your browser does not support voice input. Please use Chrome, Edge, or Safari.");
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'hi-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.start();
    recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        const inputField = parent.document.querySelector('input[data-testid="stTextInput"]');
        if (inputField) {
            inputField.value = spokenText;
            inputField.dispatchEvent(new Event('input', { bubbles: true }));
        }
        // Try to click the send button (if exists)
        const sendBtn = parent.document.querySelector('button[kind="primary"]');
        if (sendBtn) sendBtn.click();
    };
    recognition.onerror = (event) => {
        alert('Error: ' + event.error);
    };
}
</script>
<button onclick="startVoiceInput()" style="background:#007bff; color:white; border:none; border-radius:20px; padding:0.4rem 0.8rem; cursor:pointer; font-size:14px;">
🎤 Speak your question
</button>
"""
components.html(voice_html, height=50)

# ---------- Helper functions ----------
def show_gst_registration():
    st.markdown("### 📋 GST Registration – Step by Step (E‑commerce seller ke liye)")
    st.markdown(f"""
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
    c1, c2, c3 = st.columns(3)
    c1.metric("Late Fee (₹50/day)", f"₹{late_fee:,.0f}")
    c2.metric("Interest (18% p.a.)", f"₹{interest:,.0f}")
    c3.metric("Total Penalty", f"₹{total:,.0f}", delta="Jaldi bharein")
    st.info("💡 Agar aapki koi bhi sale nahi thi (nil return), toh late fee sirf ₹20/day hai.")

def show_tcs_guide():
    st.markdown("### 🏦 Amazon / Flipkart par TCS (seller ke liye)")
    st.markdown(f"""
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

# ---------- Main Header ----------
st.markdown('<div class="deployer-header"><h1>🚀 CA Deployer</h1><p>GST, ITR aur penalty ki aasaan guide (Hindi + English)</p></div>', unsafe_allow_html=True)

# ---------- Sidebar with Mascot (FIXED: fallback if image missing) ----------
with st.sidebar:
    # Check if the image file exists
    if os.path.exists("1387.png"):
        st.image("1387.png", width=180, caption="🤵 Your CA Assist")
    else:
        st.markdown("### 🤵 Your CA Assist")
        st.info("⬆️ Upload your mascot image (1387.png) if you have one.")
    
    # Dark mode toggle
    dark_toggle = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_toggle
        st.rerun()
    
    st.markdown("### 📚 Aap kya karna chahte ho?")
    task = st.selectbox("Koi ek kaam chune:", [
        "📋 GST Registration karein",
        "📝 Income Tax Return (ITR) bharein",
        "💰 Late Fee / Penalty calculate karein",
        "🏦 Amazon/Flipkart ka TCS samjhein"
    ])
    
    # Dynamic tips
    if task == "📋 GST Registration karein":
        st.sidebar.info("💡 **CA Deployer Tip:** PAN card aur address proof ready rakhein!")
    elif task == "📝 Income Tax Return (ITR) bharein":
        st.sidebar.info("💡 **CA Deployer Tip:** Pehle apna Form 26AS download karein.")
    elif task == "💰 Late Fee / Penalty calculate karein":
        st.sidebar.info("💡 **CA Deployer Tip:** Jitni jaldi file karein, utna kam penalty.")
    else:
        st.sidebar.info("💡 **CA Deployer Tip:** TCS credit claim karne ke liye GSTR-2B check karein.")

# ---------- Main content ----------
if task == "📋 GST Registration karein":
    show_gst_registration()
elif task == "📝 Income Tax Return (ITR) bharein":
    show_itr_guide()
elif task == "💰 Late Fee / Penalty calculate karein":
    show_penalty_calculator()
else:
    show_tcs_guide()

# ---------- Voice input duplicate (for convenience) ----------
st.markdown("---")
st.markdown("#### 🎤 या सीधे बोलकर सवाल पूछें:")
components.html(voice_html, height=60)

# ---------- Quick question expander ----------
with st.expander("💬 Koi chota sawaal poocho (jaise class mein)"):
    q = st.text_input("Apna sawaal likhein:", placeholder="Jaise: GST ke liye kya documents chahiye?")
    if q:
        if "document" in q.lower():
            st.info("📄 Documents: PAN card, Aadhaar card, address proof, bank statement / cancelled cheque, photo.")
        elif "due date" in q.lower() or "tarikh" in q.lower():
            st.info("📅 GSTR-3B ki last date 20th of next month. ITR ki last date 31 July (mostly).")
        elif "tcs" in q.lower():
            st.info("🏦 Amazon/Flipkart 1% TCS kaat ta hai. Aap GSTR-2B dekh kar claim kar sakte ho.")
        else:
            st.info("🚀 Main simple deployer hoon. Bade sawaal ke liye upar diye gaye topics mein se chune.")

# ---------- Footer ----------
st.caption("🚀 **CA Deployer ki salah:** GST ya ITR file karne se pehle saare documents ready rakhein. Koi doubt ho to apne kisi CA dost se pooch lein.")
