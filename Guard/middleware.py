from django.http import JsonResponse
from .models import sec_audit_log, user_input
from .security_engine import ThreatAnalyzer

class CyberGuardGlobalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract Client Network Meta-Stamps
        x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward:
            ip = x_forward.split(',')[0].strip() 
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        if request.method == 'POST':
            for key, user_text in request.POST.items():
                if key == 'csrfmiddlewaretoken':
                    continue

                is_malicious, threat_type, signature = ThreatAnalyzer.scan_payload(user_text)

                if is_malicious:
                    # Log forensic trail out-of-band (Truncate payload to 2000 chars max for DB safety)
                    sec_audit_log.objects.create(
                        attempted_payload=user_text[:2000],
                        flagged_keywords=f"{threat_type} ({signature})",
                        ip_address=ip
                    )

                    # Mark data integrity state
                    user_input.objects.create(
                        text=user_text[:2000],
                        is_safe=False
                    )

                    # Return clean JSON API error status response instead of raw HTML string
                    return JsonResponse(
                        {
                            "status": "denied",
                            "error": "SECURITY_INTERCEPT",
                            "message": "Malicious patterns identified. Footprint logged.",
                            "incident_meta": {"origin": ip, "class": threat_type}
                        },
                        status=403
                    )
            
        return self.get_response(request)