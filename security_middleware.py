import hashlib
import hmac
import time
from functools import wraps

class SecurityHeaders:
    """Add security headers to all responses"""
    
    HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    @staticmethod
    def add_headers(response):
        for key, value in SecurityHeaders.HEADERS.items():
            response.headers[key] = value
        return response

class RequestSanitizer:
    """Sanitize all incoming requests"""
    
    @staticmethod
    def sanitize_input(user_input):
        """Remove potentially dangerous patterns"""
        dangerous_patterns = [
            r"<script.*?>.*?</script>",  # XSS
            r"SELECT.*?FROM",  # SQL injection
            r"DROP\s+TABLE",  # SQL injection
            r"<.*?javascript:.*?>",  # JS injection
        ]
        
        for pattern in dangerous_patterns:
            user_input = re.sub(pattern, "[FILTERED]", user_input, flags=re.IGNORECASE)
        
        return user_input[:2000]  # Max length limit
