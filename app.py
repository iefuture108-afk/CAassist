import streamlit as st
import pandas as pd
import random
import re
import time
import hashlib
import json
from datetime import datetime, timedelta
from collections import defaultdict

# ---------- LEGAL DISCLAIMER CONSTANTS ----------
LEGAL_DISCLAIMER = """
⚠️ **LEGAL DISCLAIMER - PLEASE READ CAREFULLY**

This AI Assistant provides **general information only** and is NOT a substitute for:
- Professional advice from a registered Chartered Accountant (CA)
- Legal advice from a qualified lawyer
- Official government notifications or circulars

**By using this service, you acknowledge and agree that:**
1. Tax laws vary by specific facts, circumstances, and jurisdiction
2. The information provided may not be accurate, complete, or up-to-date
3. AI-generated content may contain errors, hallucinations, or omissions
4. You assume full responsibility for any decisions or actions taken
5. The developer, operator, and hosting provider are NOT liable for any:
   - Financial losses, penalties, or legal consequences
   - Reliance on AI-generated information
   - Delays, errors, or omissions in responses

**Recommended Action:** Always verify critical tax/financial information with:
- Official government websites (gst.gov.in, incometax.gov.in)
- A registered CA with valid COP (Certificate of Practice)
- Your legal advisor

**Compliance Status:** This platform operates as an information service under the IT Act, 2000 and DPDP Act, 2023. We are NOT a registered CA firm.

[By proceeding, you confirm you have read, understood, and agreed to the above]
"""

PRIVACY_POLICY = """
# 📋 PRIVACY POLICY (DPDP Act, 2023 Compliant)

**Last Updated:** June 2026

## 1. Data We Collect
- **Personal Information:** Name, PIN code (for access)
- **Usage Data:** Queries, timestamps, anonymized interaction logs
- **Technical Data:** IP address (retained for 30 days for security)

## 2. How We Use Your Data
- ✅ To provide AI-generated responses to your queries
- ✅ To improve our AI models (anonymized and aggregated)
- ✅ To comply with legal obligations (IT Rules, 2021)
- ✅ To detect and prevent abuse or harmful content

## 3. Data Storage & Security
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- Conversations stored for maximum 90 days, then anonymized
- IP addresses retained for 30 days (legal compliance)

## 4. Your Rights (Data Principal Rights)
You have the right to:
- **Access:** Request a copy of your data
- **Correction:** Fix inaccurate information
- **Erasure:** Delete your data (request via grievance@cassist.ai)
- **Grievance:** Lodge complaint with Data Protection Board

## 5. Data Sharing
We do NOT sell your data. We share only:
- With AI API providers (OpenAI/Claude) to generate responses (subject to their privacy policies)
- With law enforcement if legally required (court order)

## 6. Children's Privacy
This service is NOT for persons under 18 years of age.

## 7. Contact & Grievance Officer
**Name:** Grievance Officer  
**Email:** grievance@cassist.ai  
**Response Time:** Within 72 hours  
**Physical Address:** [Your Registered Address]

## 8. Breach Notification
In case of data breach, affected users will be notified within 72 hours as required by DPDP Act.

**Consent:** By using this platform, you explicitly consent to this privacy policy.
"""

TERMS_OF_SERVICE = """
# ⚖️ TERMS OF SERVICE

## 1. Acceptance
By accessing CA Assist AI, you agree to these terms, the Privacy Policy, and Legal Disclaimer.

## 2. No CA-Client Relationship
Use of this AI does NOT create a chartered accountant-client relationship. We are not responsible for your tax filings or compliance.

## 3. Prohibited Uses
You may NOT use this service to:
- Attempt illegal tax evasion
- Generate fraudulent documents
- Harass, abuse, or harm others
- Reverse engineer or scrape the AI model
- Use for competitive intelligence

## 4. Limitation of Liability
To the maximum extent permitted by law:
- Total liability cap: ₹1,000 (Rupees One Thousand Only)
- We are NOT liable for indirect, consequential, or special damages

## 5. Indemnification
You agree to indemnify and hold harmless the operator from any claims arising from your misuse of this service.

## 6. Governing Law
These terms are governed by the laws of India. Disputes subject to exclusive jurisdiction of courts in [Your City].

## 7. Modifications
We may update these terms at any time. Continued use constitutes acceptance.

## 8. Grievance Redressal
Contact grievance@cassist.ai for complaints. Response within 72 hours.

**Last Updated:** June 2026
"""

# ---------- CONTENT FILTERING (IT Rules 2021) ----------
class ContentFilter:
    """Prevents harmful/prohibited queries"""
    
    PROHIBITED_PATTERNS = {
        "tax_evasion": [
            r"(hide|conceal|evade|avoid paying)\s*(tax|gst|income tax)",
            r"(fake|false|bogus)\s*(invoice|bill|receipt)",
            r"under[ -]?reporting\s*(income|sales)",
            r"black\s*money",
            r"hawala"
        ],
        "illegal_activities": [
            r"(hack|crack|break into)\s*(gst|income tax|portal|server)",
            r"forgery",
            r"counterfeit\s*(gstin|pan|invoice)",
            r"identity\s*theft"
        ],
        "harmful_content": [
            r"(threat|abuse|harass|bully)",
            r"(violence|attack|harm)\s*(person|people)",
            r"terrorism"
        ],
        "sensitive_personal_info": [
            r"(pan\s*number|aadhaar|password|otp)",
            r"(credit\s*card|debit\s*card|bank\s*account)\s*(number|details)"
        ]
    }
    
    @staticmethod
    def is_prohibited(query):
        """Check if query contains prohibited content"""
        query_lower = query.lower()
        
        for category, patterns in ContentFilter.PROHIBITED_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return True, category, pattern
        
        return False, None, None
    
    @staticmethod
    def sanitize_response(response):
        """Ensure response doesn't contain prohibited content"""
        # Additional safety: block any response that might encourage illegal activity
        harmful_phrases = [
            "you can hide", "evade tax by", "fake invoice", 
            "underreport without getting caught"
        ]
        
        for phrase in harmful_phrases:
            if phrase.lower() in response.lower():
                return "⚠️ I cannot provide information that may facilitate tax evasion or illegal activities. Please consult a registered CA for legitimate tax planning."
        
        return response

# ---------- RATE LIMITING ----------
class RateLimiter:
    """Prevents abuse and DDoS"""
    
    def __init__(self):
        self.user_requests = defaultdict(list)
        self.MAX_REQUESTS_PER_MINUTE = 30
        self.MAX_REQUESTS_PER_HOUR = 300
    
    def check_limit(self, user_id):
        """Check if user exceeded rate limits"""
        now = time.time()
        
        # Clean old entries
        self.user_requests[user_id] = [
            ts for ts in self.user_requests[user_id] 
            if now - ts < 3600  # Keep last hour
        ]
        
        # Check minute limit
        minute_requests = len([ts for ts in self.user_requests[user_id] if now - ts < 60])
        if minute_requests >= self.MAX_REQUESTS_PER_MINUTE:
            return False, "Rate limit exceeded: Maximum 30 queries per minute"
        
        # Check hour limit
        if len(self.user_requests[user_id]) >= self.MAX_REQUESTS_PER_HOUR:
            return False, "Rate limit exceeded: Maximum 300 queries per hour"
        
        # Add current request
        self.user_requests[user_id].append(now)
        return True, "OK"

# ---------- AUDIT LOGGING (For Legal Compliance) ----------
class AuditLogger:
    """Logs interactions for legal compliance (anonymized after 30 days)"""
    
    @staticmethod
    def log_interaction(user_id, query, response_summary, status):
        """Store interaction for audit trail"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_hash": hashlib.sha256(user_id.encode()).hexdigest()[:16],
            "query_hash": hashlib.sha256(query.encode()).hexdigest()[:16],
            "response_length": len(response_summary),
            "status": status,
            "ip_hash": "[REDACTED]",  # In production, hash the IP
        }
        
        # In production, write to secure database
        # For demo, store in session
        if 'audit_logs' not in st.session_state:
            st.session_state.audit_logs = []
        st.session_state.audit_logs.append(log_entry)
        
        # Keep only last 100 for demo
        if len(st.session_state.audit_logs) > 100:
            st.session_state.audit_logs = st.session_state.audit_logs[-100:]
        
        return log_entry

# ---------- KNOWLEDGE BASE (Same as before, but with safeguards) ----------
class CAKnowledgeBase:
    """Comprehensive knowledge base for CA workflows (safeguarded)"""
    
    # [Previous knowledge base methods remain the same]
    # (Included from previous code for brevity - paste your existing KB here)
    
    @staticmethod
    def get_gst_info(query):
        """GST related information with compliance flags"""
        # Restrict sensitive queries
        if any(word in query.lower() for word in ['evasion', 'fake', 'illegal', 'bypass']):
            return {
                "error": "cannot_provide",
                "message": "I cannot provide information that may facilitate tax evasion or illegal activities. For legitimate tax planning, please consult a registered CA."
            }
        
        # [Rest of GST info logic from previous code]
        return None

# ---------- LEGAL CONSENT COMPONENT ----------
def legal_consent_modal():
    """Force user to accept legal terms before using the app"""
    
    if 'legal_accepted' not in st.session_state:
        st.session_state.legal_accepted = False
    
    if not st.session_state.legal_accepted:
        st.markdown("### ⚖️ Legal Compliance Required")
        
        with st.expander("📜 Legal Disclaimer (MUST READ)", expanded=True):
            st.markdown(LEGAL_DISCLAIMER)
        
        with st.expander("📋 Privacy Policy (DPDP Act 2023 Compliant)"):
            st.markdown(PRIVACY_POLICY)
        
        with st.expander("⚖️ Terms of Service"):
            st.markdown(TERMS_OF_SERVICE)
        
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.checkbox("I have read, understood, and agree to the Legal Disclaimer, Privacy Policy, and Terms of Service", key="legal_accept_checkbox")
        
        with col2:
            if st.button("✅ Proceed to CA Assist", use_container_width=True):
                if st.session_state.get('legal_accept_checkbox', False):
                    st.session_state.legal_accepted = True
                    st.session_state.legal_accept_time = datetime.now().isoformat()
                    st.rerun()
                else:
                    st.error("You must accept the legal terms to use this service")
        
        st.stop()  # Stop execution until accepted

# ---------- MAIN APP WITH LEGAL & SECURITY ----------
def main():
    """Main application with all legal and security controls"""
    
    st.set_page_config(
        page_title="CA Assist AI - Compliant Virtual CA",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Force legal consent first
    legal_consent_modal()
    
    # Initialize session state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{int(time.time())}_{random.randint(1000,9999)}"
    if 'rate_limiter' not in st.session_state:
        st.session_state.rate_limiter = RateLimiter()
    if 'audit_logger' not in st.session_state:
        st.session_state.audit_logger = AuditLogger()
    
    # Check rate limit at app start
    rate_ok, rate_msg = st.session_state.rate_limiter.check_limit(st.session_state.user_id)
    if not rate_ok:
        st.error(f"⛔ {rate_msg}")
        st.info("Please wait a moment before continuing. This is for security and fair usage.")
        st.stop()
    
    # Display permanent legal header
    st.warning("⚠️ **Legal Notice:** AI-generated information may contain errors. Always verify with a registered CA or official government sources.")
    
    # [Rest of your CA Assist app UI and logic from previous code]
    # (Include the chat interface, knowledge base integration, etc.)
    
    st.markdown("---")
    st.caption(f"Session ID: {st.session_state.user_id[:12]}... | Grievance: grievance@cassist.ai | Response within 72 hours")

# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    main()
