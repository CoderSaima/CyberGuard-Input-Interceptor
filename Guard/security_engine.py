import re

class ThreatAnalyzer:
    
    SQLI_PATTERN = re.compile(
        r"('(--|\#|\/\*)|(\b(SELECT|UNION|INSERT|DELETE|DROP|UPDATE|WHERE|OR|AND)\b))|(\d+=\d+)", 
        re.IGNORECASE
    )
    XSS_PATTERN = re.compile(
        r"(<script.*?>|javascript:|onerror=|onload=|htmlTag|<.*?>)", 
        re.IGNORECASE
    )

    @classmethod
    def scan_payload(cls, value: str):
        """
        Scans a string parameter for injection signatures.
        Returns (is_malicious, threat_type, matched_signature)
        """
        if not value or not isinstance(value, str):
            return False, None, None

        # Normalize whitespace variations to detect obfuscated "1 == 1"
        normalized_value = " ".join(value.split())

        if cls.XSS_PATTERN.search(normalized_value):
            return True, "XSS", "XSS Pattern Vector Match"
            
        if cls.SQLI_PATTERN.search(normalized_value) or "1=1" in normalized_value.replace(" ", ""):
            return True, "SQLI", "SQLi Logic Vector Match"

        return False, None, None
