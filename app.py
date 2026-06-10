import streamlit as st
import random
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CA Assist - Tax Guide",
    page_icon="🧾",
    layout="wide"
)

# ---------- SIMPLE CSS ----------
st.markdown("""
<style>
.user-msg {
    background-color: #e8f0fe;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    max-width: 80%;
    float: right;
    clear: both;
}
.ai-msg {
    background-color: #f1f3f4;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 8px 0;
    max-width: 80%;
    float: left;
    clear: both;
}
.chat-container {
    min-height: 400px;
    margin-bottom: 20px;
}
.govt-link {
    color: #1a73e8;
    text-decoration: none;
}
.govt-link:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ---------- GOVERNMENT LINKS DATABASE ----------
GOVT_LINKS = {
    "gst_portal": "https://www.gst.gov.in",
    "income_tax_portal": "https://www.incometax.gov.in",
    "msme_registration": "https://udyamregistration.gov.in",
    "pan_tin": "https://www.tin-nsdl.com",
    "gst_returns": "https://services.gst.gov.in/services/login",
    "e_way_bill": "https://ewaybillgst.gov.in",
    "itr_filing": "https://www.incometax.gov.in/iec/foportal/"
}

# ---------- KNOWLEDGE BASE (Only official procedures + links) ----------
def get_response(user_query):
    """Return response with government links and standard procedures"""
    
    q = user_query.lower().strip()
    
    # GST Registration
    if "gst registration" in q or "register for gst" in q or "how to get gst" in q:
        return f"""
        **📋 GST Registration Process**
        
        **Step-by-step guide:**
        1. Visit official GST portal: [{GOVT_LINKS['gst_portal']}]({GOVT_LINKS['gst_portal']})
        2. Click 'Services' → 'Registration' → 'New Registration'
        3. Enter PAN, mobile, email → Get OTP
        4. Receive Temporary Reference Number (TRN)
        5. Login with TRN → Complete Part B form
        6. Upload documents (address proof, bank statement, photo)
        7. Submit using EVC (OTP) or DSC
        8. Get ARN → GSTIN within 7 days
        
        **Documents required:**
        • PAN Card
        • Aadhaar Card
        • Business address proof
        • Bank account statement/cancelled cheque
        • Passport size photo
        
        **Cost:** ₹0 (Government fee)
        
        🔗 **Official Portal:** [gst.gov.in]({GOVT_LINKS['gst_portal']})
        """
    
    # GST Returns
    if "gst return" in q or "file gst" in q or "gstr" in q:
        return f"""
        **📅 GST Return Filing Guide**
        
        **Returns you need to file:**
        
        | Return | Due Date | What to file |
        |--------|----------|--------------|
        | GSTR-1 | 11th of next month | Sales details |
        | GSTR-3B | 20th of next month | Tax summary + payment |
        | GSTR-9 | 31st Dec (annual) | Annual return |
        
        **Step-by-step filing:**
        1. Login to [{GOVT_LINKS['gst_returns']}]({GOVT_LINKS['gst_returns']})
        2. Go to 'Returns Dashboard'
        3. Select month/year
        4. Fill GSTR-1 (invoice-wise for B2B, summary for B2C)
        5. File GSTR-1 using DSC/EVC
        6. GSTR-2B auto-populates on 14th
        7. Fill GSTR-3B (tax liability + ITC claim)
        8. Pay tax and file GSTR-3B
        
        **Late fees:** ₹50/day (with tax) or ₹20/day (nil return)
        
        🔗 **File here:** [{GOVT_LINKS['gst_returns']}]({GOVT_LINKS['gst_returns']})
        """
    
    # TCS for E-commerce
    if "tcs" in q or "marketplace" in q or "amazon" in q or "flipkart" in q:
        return f"""
        **🏦 TCS on E-commerce Sales**
        
        **What is TCS?**
        - Marketplaces deduct **1% TCS** (0.5% CGST + 0.5% SGST or 1% IGST)
        - Deducted before payout to you
        
        **How to claim TCS credit:**
        1. Download GSTR-2A from [{GOVT_LINKS['gst_portal']}]({GOVT_LINKS['gst_portal']})
        2. Check TCS credit under 'TCS Credit' section
        3. Auto-populates in GSTR-3B
        4. Use this credit to pay your GST liability
        
        **Important checklist:**
        ✅ Verify marketplace GSTIN in your settlement report
        ✅ Download GSTR-2B on 14th of every month
        ✅ Reconcile TCS before filing GSTR-3B
        ✅ Report mismatches to marketplace within 30 days
        
        🔗 **Check TCS credit:** [gst.gov.in]({GOVT_LINKS['gst_portal']})
        """
    
    # Income Tax - New Regime vs Old Regime
    if "income tax slab" in q or "tax rate" in q or "new regime" in q or "old regime" in q:
        return f"""
        **💰 Income Tax Slabs (FY 2024-25)**
        
        **New Tax Regime (Default):**
        
        | Income Range | Tax Rate |
        |--------------|----------|
        | ₹0 - ₹3,00,000 | 0% |
        | ₹3,00,001 - ₹6,00,000 | 5% |
        | ₹6,00,001 - ₹9,00,000 | 10% |
        | ₹9,00,001 - ₹12,00,000 | 15% |
        | ₹12,00,001 - ₹15,00,000 | 20% |
        | Above ₹15,00,000 | 30% |
        
        **Old Tax Regime (Opt-in):**
        
        | Income Range | Tax Rate |
        |--------------|----------|
        | ₹0 - ₹2,50,000 | 0% |
        | ₹2,50,001 - ₹5,00,000 | 5% |
        | ₹5,00,001 - ₹10,00,000 | 20% |
        | Above ₹10,00,000 | 30% |
        
        **Standard Deduction:** ₹50,000 (salaried)
        
        🔗 **Official portal:** [{GOVT_LINKS['income_tax_portal']}]({GOVT_LINKS['income_tax_portal']})
        """
    
    # ITR Filing
    if "itr filing" in q or "file itr" in q or "income tax return" in q:
        return f"""
        **📝 ITR Filing Guide**
        
        **Which ITR form to use:**
        
        | Form | Who can file |
        |------|--------------|
        | ITR-1 (Sahaj) | Salary, one house property, income < ₹50L |
        | ITR-2 | Capital gains, multiple house properties |
        | ITR-3 | Business/professional income |
        | ITR-4 (Sugam) | Presumptive taxation (44AD/44ADA) |
        
        **Due Dates:**
        - Without audit: **31st July**
        - With audit: **31st October**
        
        **Step-by-step:**
        1. Login to [{GOVT_LINKS['income_tax_portal']}]({GOVT_LINKS['income_tax_portal']})
        2. Go to 'e-File' → 'Income Tax Return'
        3. Select Assessment Year (2025-26)
        4. Choose correct ITR form
        5. Fill details (can auto-fill from Form 26AS)
        6. Validate and submit
        7. E-verify using Aadhaar OTP, Net banking, or DSC
        
        🔗 **File ITR:** [{GOVT_LINKS['income_tax_portal']}]({GOVT_LINKS['income_tax_portal']})
        """
    
    # TDS
    if "tds" in q and "deduction" not in q:
        return f"""
        **📌 TDS (Tax Deducted at Source) Guide**
        
        **Common TDS rates:**
        
        | Payment Type | TDS Rate | Section |
        |--------------|----------|---------|
        | Salary | Slab rate | 192 |
        | Contractor payment | 1% (individual) / 2% (others) | 194C |
        | Rent (plant/machinery) | 2% | 194-I |
        | Rent (land/building) | 10% | 194-I |
        | Professional fees | 10% | 194J |
        | Interest (other than securities) | 10% | 194A |
        
        **Important due dates:**
        - TDS Deposit: **7th of next month**
        - TDS Return (24Q/26Q): **31st of next month**
        - TDS Certificate (Form 16/16A): Within 15 days of return filing
        
        🔗 **TDS portal:** [tin-nsdl.com]({GOVT_LINKS['pan_tin']})
        """
    
    # 80C Deductions
    if "80c" in q or "tax saving" in q or "deduction" in q:
        return f"""
        **💡 Section 80C Deductions (Max ₹1,50,000)**
        
        **Eligible investments/expenses:**
        - ✅ Life Insurance Premium (LIC)
        - ✅ PPF (Public Provident Fund)
        - ✅ ELSS (Equity Linked Savings Scheme)
        - ✅ 5-year Fixed Deposit (Post Office/Bank)
        - ✅ NSC (National Savings Certificate)
        - ✅ Sukanya Samriddhi Yojana
        - ✅ Tuition fees (children, max 2 kids)
        - ✅ Home loan principal repayment
        - ✅ NPS (up to ₹50,000 additional under 80CCD(1B))
        
        **Other popular deductions:**
        - **80D:** Health insurance (₹25,000 self, ₹50,000 senior citizens)
        - **80E:** Education loan interest (no limit)
        - **80G:** Donations (50% or 100% of amount)
        - **80TTA:** Interest on savings account (₹10,000)
        
        🔗 **Official source:** [incometax.gov.in]({GOVT_LINKS['income_tax_portal']})
        """
    
    # e-Way Bill
    if "eway" in q or "e-way bill" in q:
        return f"""
        **🚛 e-Way Bill Guide**
        
        **When required:**
        - Goods value > ₹50,000
        - Inter-state movement of goods
        - Intra-state (varies by state, typically > ₹1 lakh)
        
        **How to generate:**
        1. Login to [{GOVT_LINKS['e_way_bill']}]({GOVT_LINKS['e_way_bill']})
        2. Enter GSTIN of supplier & recipient
        3. Enter invoice details (number, date, value)
        4. Enter HSN code and quantity
        5. Enter transporter details (vehicle number)
        6. Generate e-Way Bill (valid for based on distance)
        
        **Validity:**
        - Up to 100 km: 1 day
        - 100-200 km: 3 days
        - 200-500 km: 5 days
        - Every additional 200 km: +1 day
        
        🔗 **Generate here:** [{GOVT_LINKS['e_way_bill']}]({GOVT_LINKS['e_way_bill']})
        """
    
    # MSME Registration
    if "msme" in q or "udyam" in q or "small business registration" in q:
        return f"""
        **🏭 MSME/Udyam Registration**
        
        **Benefits:**
        - Priority sector lending
        - Interest rate subsidy (2-3%)
        - Government tender preference
        - Protection against delayed payments
        - Subsidy on patent/industry registration
        
        **Eligibility:**
        
        | Category | Investment (Plant & Machinery) | Turnover |
        |----------|-------------------------------|----------|
        | Micro | ≤ ₹1 crore | ≤ ₹5 crore |
        | Small | ≤ ₹10 crore | ≤ ₹50 crore |
        | Medium | ≤ ₹50 crore | ≤ ₹250 crore |
        
        **Process:**
        1. Visit [{GOVT_LINKS['msme_registration']}]({GOVT_LINKS['msme_registration']})
        2. Enter Aadhaar number
        3. Fill business details (name, address, bank)
        4. Enter investment and turnover
        5. Submit → Get Udyam Registration Certificate instantly
        
        🔗 **Register:** [udyamregistration.gov.in]({GOVT_LINKS['msme_registration']})
        """
    
    # Late fee / Penalty
    if "penalty" in q or "late fee" in q or "interest" in q:
        return f"""
        **⚠️ GST Late Fee & Interest**
        
        **GST Late Fees:**
        - GSTR-3B (with tax): ₹50/day (₹25 CGST + ₹25 SGST)
        - GSTR-3B (nil return): ₹20/day (₹10 CGST + ₹10 SGST)
        - GSTR-1: ₹50/day (₹25 CGST + ₹25 SGST)
        - Maximum late fee: ₹5,000 per return
        
        **Interest:**
        - 18% per annum on tax amount overdue
        - Calculated from due date to actual payment date
        
        **Example:**
        If tax due is ₹10,000 and delayed by 30 days:
        - Late fee: ₹50 × 30 = ₹1,500
        - Interest: ₹10,000 × 18% × (30/365) = ₹148
        - Total penalty: ₹1,648
        
        **How to pay penalty:**
        1. Login to gst.gov.in
        2. File pending return (will auto-calculate penalty)
        3. Pay via online banking/credit card
        4. Download acknowledgment
        
        🔗 **File pending returns:** [{GOVT_LINKS['gst_portal']}]({GOVT_LINKS['gst_portal']})
        """
    
    # Input Tax Credit
    if "itc" in q or "input tax credit" in q:
        return f"""
        **🔄 Input Tax Credit (ITC) Guide**
        
        **What is ITC?**
        Tax you paid on purchases can be reduced from tax you collect on sales.
        
        **Eligibility conditions:**
        ✅ Must have valid tax invoice
        ✅ Goods/services must be received
        ✅ Supplier must have filed return and paid tax
        ✅ ITC appears in GSTR-2B
        ✅ Used for business purpose only
        
        **ITC that is BLOCKED (cannot claim):**
        ❌ Motor vehicles (except for further sale/transport business)
        ❌ Food & beverages
        ❌ Health services (medical insurance, gym)
        ❌ Rent-a-cab service
        ❌ Membership fees (clubs, health clubs)
        ❌ Works contract for immovable property
        
        **How to claim:**
        1. Ensure supplier files GSTR-1
        2. Check GSTR-2B (available on 14th of every month)
        3. Match ITC with your purchase register
        4. Claim in GSTR-3B
        5. Keep invoices ready for audit (7 years)
        
        🔗 **Check your ITC:** [{GOVT_LINKS['gst_portal']}]({GOVT_LINKS['gst_portal']}) → 'Returns' → 'GSTR-2B'
        """
    
    # Help / Default
    return f"""
    **🤖 CA Assist - Your Tax Guide**
    
    I can help you with these topics:
    
    | Topic | What to ask |
    |-------|-------------|
    | 📋 **GST Registration** | "How to register for GST?" |
    | 📅 **GST Returns** | "How to file GSTR-3B?" |
    | 🏦 **TCS on E-commerce** | "TCS on Amazon/Flipkart" |
    | 💰 **Income Tax** | "Income tax slab 2024" |
    | 📝 **ITR Filing** | "How to file ITR?" |
    | 💡 **Tax Saving** | "80C deductions list" |
    | ⚠️ **Penalty** | "Late fee for GSTR-3B" |
    | 🏭 **MSME** | "MSME registration" |
    | 🚛 **e-Way Bill** | "How to generate e-Way Bill?" |
    | 🔄 **ITC** | "What is Input Tax Credit?" |
    
    **Just type your question above!** 
    
    🔗 **All information includes links to official government portals.**
    """

# ---------- SESSION STATE ----------
def init():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm CA Assist. Ask me anything about GST, Income Tax, or business compliance. I'll guide you with official government links and standard procedures."
        })

# ---------- MAIN APP ----------
def main():
    init()
    
    # Header
    st.title("🧾 CA Assist")
    st.caption("Your guide to GST, Income Tax & Business Compliance")
    st.divider()
    
    # Chat display
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg"><b>You:</b><br/>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-msg"><b>🤖 CA Assist:</b><br/>{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Input area
    st.divider()
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Ask your question here:", placeholder="e.g., How to register for GST?", key="input", label_visibility="collapsed")
    
    with col2:
        send_btn = st.button("Send", use_container_width=True)
    
    # Suggested quick questions
    st.caption("💡 Quick questions:")
    quick_cols = st.columns(4)
    quick_questions = [
        "GST registration process",
        "Income tax slab rates",
        "How to file GSTR-3B?",
        "TCS on Amazon sales"
    ]
    
    for i, q in enumerate(quick_questions):
        with quick_cols[i]:
            if st.button(q, use_container_width=True):
                user_input = q
    
    # Process input
    if send_btn and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        response = get_response(user_input)
        
        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to refresh chat
        st.rerun()
    
    # Footer
    st.divider()
    st.caption("🔗 All information includes official government portal links. Always verify on government websites.")
    st.caption("📌 GST Portal: gst.gov.in | Income Tax Portal: incometax.gov.in")

# ---------- RUN ----------
if __name__ == "__main__":
    main()
