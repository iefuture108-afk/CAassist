import streamlit as st
import random
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CA Assist - Virtual Chartered Accountant",
    page_icon="⚖️",
    layout="wide"
)

# ---------- CUSTOM CSS FOR CA OFFICE LOOK ----------
st.markdown("""
<style>
/* CA Office Theme */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Header */
.ca-header {
    background: linear-gradient(135deg, #1a3c34 0%, #2d5a4c 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.ca-header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 600;
}

.ca-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-size: 0.9rem;
}

/* Badge */
.ca-badge {
    background: linear-gradient(135deg, #c9a03d 0%, #b8860b 100%);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    color: white;
    display: inline-block;
    margin-bottom: 0.5rem;
}

/* Chat bubbles */
.user-message {
    background: #e8f0fe;
    padding: 12px 18px;
    border-radius: 20px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    float: right;
    clear: both;
    border-bottom-right-radius: 5px;
    color: #1a3c34;
    font-size: 0.95rem;
}

.assistant-message {
    background: white;
    padding: 12px 18px;
    border-radius: 20px;
    margin: 8px auto 8px 0;
    max-width: 75%;
    float: left;
    clear: both;
    border-left: 3px solid #c9a03d;
    border-bottom-left-radius: 5px;
    color: #2d3748;
    font-size: 0.95rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Sidebar */
.sidebar-ca {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}

/* Quick buttons */
.stButton > button {
    background: #1a3c34;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #2d5a4c;
    transform: scale(1.02);
}

/* Footer */
.ca-footer {
    text-align: center;
    padding: 1rem;
    font-size: 0.75rem;
    color: #6c757d;
    border-top: 1px solid #dee2e6;
    margin-top: 1rem;
}

/* Table styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
}

th {
    background: #f0f2f6;
    padding: 8px;
    text-align: left;
}

td {
    padding: 8px;
    border-bottom: 1px solid #e0e4e8;
}
</style>
""", unsafe_allow_html=True)

# ---------- GOVERNMENT LINKS ----------
GOVT_LINKS = {
    "gst_portal": "https://www.gst.gov.in",
    "income_tax_portal": "https://www.incometax.gov.in",
    "msme_registration": "https://udyamregistration.gov.in",
    "pan_tin": "https://www.tin-nsdl.com",
    "gst_returns": "https://services.gst.gov.in/services/login",
    "e_way_bill": "https://ewaybillgst.gov.in",
    "itr_filing": "https://www.incometax.gov.in/iec/foportal/",
    "gst_search": "https://services.gst.gov.in/services/searchtp",
    "e_invoice": "https://einvoice.gst.gov.in"
}

# ---------- RESPONSE GENERATION ----------
def get_response(user_query):
    """Generate response based on user query"""
    
    q = user_query.lower().strip()
    
    # Greeting
    if any(word in q for word in ["hi", "hello", "hey", "namaste", "good morning"]):
        return f"""
        <span class="ca-badge">⚖️ WELCOME</span><br><br>
        <strong>Namaste! I'm your virtual CA.</strong><br><br>
        
        I can help you with:
        <br>• 📋 GST Registration & Returns
        <br>• 💰 Income Tax & ITR Filing
        <br>• 🏦 TCS on E-commerce (Amazon/Flipkart)
        <br>• 💡 Tax Saving (80C, 80D)
        <br>• 📅 Due Dates & Penalties
        <br>• 🚛 e-Way Bill Generation
        <br>• 🏭 MSME/Udyam Registration
        
        <br><strong>What would you like to know today?</strong>
        """
    
    # GST Registration
    if any(word in q for word in ["gst registration", "register for gst", "how to get gst", "gst number", "gst apply"]):
        return f"""
        <span class="ca-badge">📋 GST REGISTRATION GUIDE</span><br><br>
        
        <strong>📌 ELIGIBILITY:</strong>
        <br>• E-commerce sellers: <strong>Mandatory</strong> (₹0 threshold)
        <br>• Normal businesses: ₹40 lakhs (goods) / ₹20 lakhs (services)
        
        <br><br><strong>📝 DOCUMENTS REQUIRED:</strong>
        <br>✓ PAN Card
        <br>✓ Aadhaar Card
        <br>✓ Business Address Proof
        <br>✓ Bank Account Statement
        <br>✓ Passport Size Photo
        
        <br><br><strong>📋 STEP-BY-STEP PROCESS:</strong>
        <br>1️⃣ Visit: <a href='{GOVT_LINKS['gst_portal']}' target='_blank'><strong>{GOVT_LINKS['gst_portal']}</strong></a>
        <br>2️⃣ Click 'Services' → 'Registration' → 'New Registration'
        <br>3️⃣ Fill Part A (PAN verification) → Get OTP
        <br>4️⃣ Receive Temporary Reference Number (TRN)
        <br>5️⃣ Login with TRN → Complete Part B form
        <br>6️⃣ Upload all documents
        <br>7️⃣ Submit using EVC (OTP on registered mobile)
        <br>8️⃣ Get ARN → GSTIN within 7 working days
        
        <br><br><strong>💰 GOVERNMENT FEE:</strong> ₹0 (Free)
        
        <br><br><strong>🔗 START REGISTRATION:</strong> <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>{GOVT_LINKS['gst_portal']}</a>
        """
    
    # GST Returns
    if any(word in q for word in ["gst return", "file gst", "gstr", "return filing", "gstr-1", "gstr-3b"]):
        return f"""
        <span class="ca-badge">📅 GST RETURN FILING</span><br><br>
        
        <strong>📊 RETURNS TO FILE:</strong>
        <br>
        <table>
            <tr><th>Return</th><th>Due Date</th><th>Details</th></tr>
            <tr><td>GSTR-1</td><td>11th of next month</td><td>Sales (B2B invoice-wise, B2C summary)</td></tr>
            <tr><td>GSTR-3B</td><td>20th of next month</td><td>Tax liability + ITC claim</td></tr>
            <tr><td>GSTR-9</td><td>31st December</td><td>Annual return</td></tr>
        </table>
        
        <br><strong>📝 FILING PROCESS:</strong>
        <br>1️⃣ Login: <a href='{GOVT_LINKS['gst_returns']}' target='_blank'>{GOVT_LINKS['gst_returns']}</a>
        <br>2️⃣ Go to 'Returns Dashboard' → Select month/year
        <br>3️⃣ Prepare GSTR-1 (invoice details)
        <br>4️⃣ File GSTR-1 using EVC/DSC
        <br>5️⃣ GSTR-2B auto-populates on 14th
        <br>6️⃣ Prepare GSTR-3B with tax calculation
        <br>7️⃣ Pay tax online
        <br>8️⃣ File GSTR-3B → Download acknowledgment
        
        <br><br><strong>⚠️ LATE FEES:</strong>
        <br>• With tax: ₹50/day (₹25 CGST + ₹25 SGST)
        <br>• Nil return: ₹20/day (₹10 CGST + ₹10 SGST)
        <br>• Maximum: ₹5,000 per return
        
        <br><br><strong>🔗 FILE RETURNS:</strong> <a href='{GOVT_LINKS['gst_returns']}' target='_blank'>{GOVT_LINKS['gst_returns']}</a>
        """
    
    # TCS for E-commerce
    if any(word in q for word in ["tcs", "marketplace", "amazon", "flipkart", "meesho", "e-commerce", "online seller"]):
        return f"""
        <span class="ca-badge">🏦 TCS ON E-COMMERCE (Section 52)</span><br><br>
        
        <strong>📊 TCS RATE:</strong> <strong>1%</strong> on net taxable value
        <br>• Intra-state: 0.5% CGST + 0.5% SGST
        <br>• Inter-state: 1% IGST
        
        <br><br><strong>✅ HOW TO CLAIM TCS CREDIT:</strong>
        <br>1️⃣ Download settlement report from your marketplace
        <br>2️⃣ Verify TCS deducted (should be 1% of taxable value)
        <br>3️⃣ Wait for <strong>14th of next month</strong>
        <br>4️⃣ Download <strong>GSTR-2B</strong> from GST Portal
        <br>5️⃣ Check 'TCS Credit' section
        <br>6️⃣ Match with marketplace report
        <br>7️⃣ TCS auto-populates in GSTR-3B
        <br>8️⃣ Use this credit to pay your GST liability
        
        <br><br><strong>⚠️ IMPORTANT CHECKLIST:</strong>
        <br>✓ Verify marketplace GSTIN in settlement report
        <br>✓ Download GSTR-2B on 14th every month
        <br>✓ Reconcile TCS BEFORE filing GSTR-3B
        <br>✓ Report mismatches within 30 days
        
        <br><br><strong>🔗 CHECK TCS CREDIT:</strong> <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>GST Portal → Returns → GSTR-2B</a>
        """
    
    # Income Tax Slabs
    if any(word in q for word in ["income tax slab", "tax rate", "new regime", "old regime", "tax percentage", "income tax rate"]):
        return f"""
        <span class="ca-badge">💰 INCOME TAX SLABS (FY 2024-25)</span><br><br>
        
        <strong>📊 NEW TAX REGIME (Default):</strong>
        <table>
            <tr><th>Income Range</th><th>Tax Rate</th></tr>
            <tr><td>₹0 - ₹3,00,000</td><td>0%</td></tr>
            <tr><td>₹3,00,001 - ₹6,00,000</td><td>5%</td></tr>
            <tr><td>₹6,00,001 - ₹9,00,000</td><td>10%</td></tr>
            <tr><td>₹9,00,001 - ₹12,00,000</td><td>15%</td></tr>
            <tr><td>₹12,00,001 - ₹15,00,000</td><td>20%</td></tr>
            <tr><td>Above ₹15,00,000</td><td>30%</td></tr>
        </table>
        
        <br><strong>📊 OLD TAX REGIME (Opt-in):</strong>
        <table>
            <tr><th>Income Range</th><th>Tax Rate</th></tr>
            <tr><td>₹0 - ₹2,50,000</td><td>0%</td></tr>
            <tr><td>₹2,50,001 - ₹5,00,000</td><td>5%</td></tr>
            <tr><td>₹5,00,001 - ₹10,00,000</td><td>20%</td></tr>
            <tr><td>Above ₹10,00,000</td><td>30%</td></tr>
        </table>
        
        <br><strong>💡 ADDITIONAL BENEFITS:</strong>
        <br>• Standard Deduction: ₹50,000 (salaried)
        <br>• Rebate 87A: Up to ₹25,000 (income up to ₹7 lakhs)
        
        <br><br><strong>🔗 OFFICIAL PORTAL:</strong> <a href='{GOVT_LINKS['income_tax_portal']}' target='_blank'>{GOVT_LINKS['income_tax_portal']}</a>
        """
    
    # ITR Filing
    if any(word in q for word in ["itr filing", "file itr", "income tax return", "itr form", "file income tax"]):
        return f"""
        <span class="ca-badge">📝 ITR FILING GUIDE</span><br><br>
        
        <strong>📌 WHICH ITR FORM?</strong>
        <table>
            <tr><th>Form</th><th>For</th></tr>
            <tr><td>ITR-1 (Sahaj)</td><td>Salary, one house property, other sources (income ≤ ₹50L)</td></tr>
            <tr><td>ITR-2</td><td>Capital gains, multiple house properties, foreign assets</td></tr>
            <tr><td>ITR-3</td><td>Business or professional income</td></tr>
            <tr><td>ITR-4 (Sugam)</td><td>Presumptive taxation (44AD/44ADA)</td></tr>
        </table>
        
        <br><strong>📅 DUE DATES:</strong>
        <br>• Without tax audit: <strong>31st July</strong>
        <br>• With tax audit: <strong>31st October</strong>
        
        <br><br><strong>📝 FILING PROCESS:</strong>
        <br>1️⃣ Login: <a href='{GOVT_LINKS['income_tax_portal']}' target='_blank'>{GOVT_LINKS['income_tax_portal']}</a>
        <br>2️⃣ 'e-File' → 'Income Tax Return'
        <br>3️⃣ Select Assessment Year (2025-26)
        <br>4️⃣ Choose correct ITR form
        <br>5️⃣ Fill details (auto-fill from Form 26AS)
        <br>6️⃣ Submit and e-Verify (Aadhaar OTP/Net banking)
        
        <br><br><strong>🔗 FILE ITR:</strong> <a href='{GOVT_LINKS['itr_filing']}' target='_blank'>{GOVT_LINKS['itr_filing']}</a>
        """
    
    # 80C Deductions
    if any(word in q for word in ["80c", "tax saving", "deduction", "save tax", "investment", "tax save"]):
        return f"""
        <span class="ca-badge">💡 TAX SAVING (SECTION 80C)</span><br><br>
        
        <strong>📌 SECTION 80C (Max ₹1,50,000):</strong>
        <br>✓ Life Insurance Premium (LIC)
        <br>✓ Public Provident Fund (PPF)
        <br>✓ ELSS Mutual Funds (Lock-in 3 years)
        <br>✓ 5-Year Fixed Deposit
        <br>✓ National Savings Certificate (NSC)
        <br>✓ Sukanya Samriddhi Yojana
        <br>✓ Tuition Fees (children, max 2 kids)
        <br>✓ Home Loan Principal Repayment
        <br>✓ NPS (Additional ₹50,000 under 80CCD(1B))
        
        <br><br><strong>📌 OTHER DEDUCTIONS:</strong>
        <br>• <strong>80D:</strong> Health Insurance (₹25,000 self, ₹50,000 senior citizens)
        <br>• <strong>80E:</strong> Education Loan Interest (No limit)
        <br>• <strong>80G:</strong> Donations (50% or 100%)
        <br>• <strong>24(b):</strong> Home Loan Interest (₹2,00,000)
        
        <br><br><strong>💡 TIP:</strong> Invest before March 31st to claim deductions for the year.
        
        <br><br><strong>🔗 OFFICIAL SOURCE:</strong> <a href='{GOVT_LINKS['income_tax_portal']}' target='_blank'>Income Tax Portal</a>
        """
    
    # TDS
    if "tds" in q and "deduction" not in q:
        return f"""
        <span class="ca-badge">📌 TDS (TAX DEDUCTED AT SOURCE)</span><br><br>
        
        <strong>📊 COMMON TDS RATES:</strong>
        <table>
            <tr><th>Payment Type</th><th>TDS Rate</th><th>Section</th></tr>
            <tr><td>Salary</td><td>Slab Rate</td><td>192</td></tr>
            <tr><td>Contractor Payment</td><td>1% / 2%</td><td>194C</td></tr>
            <tr><td>Rent (Land/Building)</td><td>10%</td><td>194-I</td></tr>
            <tr><td>Professional Fees</td><td>10%</td><td>194J</td></tr>
            <tr><td>Interest (Others)</td><td>10%</td><td>194A</td></tr>
        </table>
        
        <br><strong>📅 IMPORTANT DATES:</strong>
        <br>• TDS Deposit: <strong>7th of next month</strong>
        <br>• TDS Return (24Q/26Q): <strong>31st of next month</strong>
        
        <br><br><strong>🔗 TDS PORTAL:</strong> <a href='{GOVT_LINKS['pan_tin']}' target='_blank'>{GOVT_LINKS['pan_tin']}</a>
        """
    
    # e-Way Bill
    if any(word in q for word in ["eway", "e-way bill", "eway bill", "transport"]):
        return f"""
        <span class="ca-badge">🚛 E-WAY BILL</span><br><br>
        
        <strong>📌 WHEN REQUIRED:</strong>
        <br>• Goods value > ₹50,000
        <br>• Inter-state movement of goods
        <br>• Intra-state (varies by state)
        
        <br><br><strong>📝 HOW TO GENERATE:</strong>
        <br>1️⃣ Visit: <a href='{GOVT_LINKS['e_way_bill']}' target='_blank'>{GOVT_LINKS['e_way_bill']}</a>
        <br>2️⃣ Enter GSTIN of supplier & recipient
        <br>3️⃣ Enter invoice details
        <br>4️⃣ Enter HSN code and quantity
        <br>5️⃣ Enter vehicle number
        <br>6️⃣ Generate e-Way Bill
        
        <br><br><strong>⏰ VALIDITY:</strong>
        <br>• Up to 100 km: 1 day
        <br>• 100-200 km: 3 days
        <br>• 200-500 km: 5 days
        <br>• Every +200 km: +1 day
        
        <br><br><strong>🔗 GENERATE HERE:</strong> <a href='{GOVT_LINKS['e_way_bill']}' target='_blank'>{GOVT_LINKS['e_way_bill']}</a>
        """
    
    # MSME Registration
    if any(word in q for word in ["msme", "udyam", "small business", "ssi", "msme registration"]):
        return f"""
        <span class="ca-badge">🏭 MSME / UDYAM REGISTRATION</span><br><br>
        
        <strong>✅ BENEFITS:</strong>
        <br>• Priority sector lending
        <br>• Interest subsidy (2-3%)
        <br>• Government tender preference
        <br>• Protection against delayed payments
        
        <br><br><strong>📊 ELIGIBILITY:</strong>
        <table>
            <tr><th>Category</th><th>Investment</th><th>Turnover</th></tr>
            <tr><td>Micro</td><td>≤ ₹1 crore</td><td>≤ ₹5 crore</td></tr>
            <tr><td>Small</td><td>≤ ₹10 crore</td><td>≤ ₹50 crore</td></tr>
            <tr><td>Medium</td><td>≤ ₹50 crore</td><td>≤ ₹250 crore</td></tr>
        </table>
        
        <br><strong>📝 PROCESS:</strong>
        <br>1️⃣ Visit: <a href='{GOVT_LINKS['msme_registration']}' target='_blank'>{GOVT_LINKS['msme_registration']}</a>
        <br>2️⃣ Click 'For New Entrepreneurs'
        <br>3️⃣ Enter Aadhaar number
        <br>4️⃣ Fill business details
        <br>5️⃣ Submit → Get Udyam Certificate instantly
        
        <br><br><strong>💰 COST:</strong> ₹0 (Free)
        
        <br><br><strong>🔗 REGISTER HERE:</strong> <a href='{GOVT_LINKS['msme_registration']}' target='_blank'>{GOVT_LINKS['msme_registration']}</a>
        """
    
    # Input Tax Credit
    if any(word in q for word in ["itc", "input tax credit", "tax credit"]):
        return f"""
        <span class="ca-badge">🔄 INPUT TAX CREDIT (ITC)</span><br><br>
        
        <strong>📌 WHAT IS ITC?</strong>
        <br>Tax paid on purchases can be reduced from tax collected on sales.
        
        <br><br><strong>✅ ELIGIBILITY:</strong>
        <br>✓ Valid tax invoice
        <br>✓ Goods/services received
        <br>✓ Supplier filed return & paid tax
        <br>✓ ITC appears in GSTR-2B
        <br>✓ Used for business only
        
        <br><br><strong>❌ BLOCKED CREDITS:</strong>
        <br>• Motor vehicles (except transport business)
        <br>• Food & beverages
        <br>• Health services
        <br>• Membership fees
        
        <br><br><strong>📝 HOW TO CLAIM:</strong>
        <br>1️⃣ Check GSTR-2B (available on 14th)
        <br>2️⃣ Match ITC with purchase register
        <br>3️⃣ Claim in GSTR-3B
        <br>4️⃣ Keep invoices for 7 years
        
        <br><br><strong>🔗 CHECK ITC:</strong> <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>GST Portal → Returns → GSTR-2B</a>
        """
    
    # Penalty / Late Fee
    if any(word in q for word in ["penalty", "late fee", "interest", "late filing"]):
        return f"""
        <span class="ca-badge">⚠️ GST LATE FEES & PENALTY</span><br><br>
        
        <strong>📊 LATE FEES:</strong>
        <br>• GSTR-3B (with tax): ₹50/day (₹25 CGST + ₹25 SGST)
        <br>• GSTR-3B (nil return): ₹20/day (₹10 CGST + ₹10 SGST)
        <br>• GSTR-1: ₹50/day
        <br>• Maximum: ₹5,000 per return
        
        <br><br><strong>💰 INTEREST:</strong>
        <br>• 18% per annum on tax amount overdue
        
        <br><br><strong>📝 EXAMPLE:</strong>
        <br>Tax due: ₹10,000 | Delay: 30 days
        <br>• Late fee: ₹50 × 30 = ₹1,500
        <br>• Interest: ₹10,000 × 18% × (30/365) = ₹148
        <br>• Total penalty: ₹1,648
        
        <br><br><strong>🔗 FILE PENDING RETURNS:</strong> <a href='{GOVT_LINKS['gst_portal']}' target='_blank'>{GOVT_LINKS['gst_portal']}</a>
        """
    
    # Default response
    return f"""
    <span class="ca-badge">⚖️ CA ASSIST</span><br><br>
    
    <strong>I can help you with these topics:</strong>
    <br><br>
    
    <strong>📋 GST</strong>
    <br>• "GST registration process"
    <br>• "How to file GSTR-3B?"
    <br>• "GSTR-1 due date"
    
    <br><strong>💰 Income Tax</strong>
    <br>• "Income tax slab 2025"
    <br>• "How to file ITR?"
    <br>• "80C deductions list"
    
    <br><strong>🏦 E-commerce Seller</strong>
    <br>• "TCS on Amazon"
    <br>• "GST for Flipkart seller"
    <br>• "Marketplace TCS credit"
    
    <br><strong>📅 Compliance</strong>
    <br>• "GST late fee penalty"
    <br>• "TDS due dates"
    <br>• "e-Way bill generation"
    
    <br><br><strong>🔗 Official Portals:</strong>
    <br>• GST: {GOVT_LINKS['gst_portal']}
    <br>• Income Tax: {GOVT_LINKS['income_tax_portal']}
    <br>• MSME: {GOVT_LINKS['msme_registration']}
    
    <br><br><em>Just type your question above! All guidance includes official government links.</em>
    """

# ---------- SESSION STATE ----------
def init_session():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": get_response("hello")
        })

# ---------- MAIN APP ----------
def main():
    init_session()
    
    # Header
    st.markdown("""
    <div class="ca-header">
        <h1>⚖️ CA Assist</h1>
        <p>Your Virtual Chartered Accountant - GST, Income Tax & Compliance Guide</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        # Chat display area
        chat_container = st.container()
        
        with chat_container:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-message"><strong>You:</strong><br/>{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message"><strong>🤵 CA Assist:</strong><br/>{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Input area
        st.markdown("---")
        
        col_input, col_btn = st.columns([4, 1])
        
        with col_input:
            user_input = st.text_input("", placeholder="Ask your question here...", key="input", label_visibility="collapsed")
        
        with col_btn:
            send_btn = st.button("Send 📤", use_container_width=True)
        
        # Quick questions
        st.markdown("**💡 Quick questions:**")
        quick_cols = st.columns(4)
        quick_questions = [
            "GST registration process",
            "Income tax slab 2025",
            "TCS on Amazon",
            "80C deductions"
        ]
        
        for i, q in enumerate(quick_questions):
            with quick_cols[i]:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    user_input = q
        
        # Process input
        if send_btn and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get response
            response = get_response(user_input)
            
            # Add assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="sidebar-ca">
            <h4>🔗 Direct Links</h4>
            <ul style="list-style: none; padding-left: 0;">
                <li>📋 <a href="https://www.gst.gov.in" target="_blank">GST Portal</a></li>
                <li>💰 <a href="https://www.incometax.gov.in" target="_blank">Income Tax Portal</a></li>
                <li>🏭 <a href="https://udyamregistration.gov.in" target="_blank">MSME Registration</a></li>
                <li>🚛 <a href="https://ewaybillgst.gov.in" target="_blank">e-Way Bill</a></li>
                <li>📝 <a href="https://www.tin-nsdl.com" target="_blank">TDS Portal</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-ca">
            <h4>📌 Popular Topics</h4>
            <ul style="list-style: none; padding-left: 0;">
                <li>✅ GST Registration</li>
                <li>✅ GSTR-3B Filing</li>
                <li>✅ TCS on E-commerce</li>
                <li>✅ ITR Filing Guide</li>
                <li>✅ 80C Tax Saving</li>
                <li>✅ e-Way Bill</li>
                <li>✅ Late Fee Penalty</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-ca">
            <h4>📅 Today's Tip</h4>
            <p>GSTR-3B is due by <strong>20th</strong> of every month. File on time to avoid ₹50/day late fee.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="ca-footer">
        ⚖️ CA Assist provides guidance only. Final filings must be done on official government portals.
        <br>🔗 All links redirect to official government websites (gst.gov.in | incometax.gov.in)
    </div>
    """, unsafe_allow_html=True)

# ---------- RUN ----------
if __name__ == "__main__":
    main()
