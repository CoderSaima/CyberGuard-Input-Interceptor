from .models import sec_audit_log, user_input
from django.http import HttpResponse

class CyberGuardGlobalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward:
            ip = x_forward.split(',')[0].strip() 
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        if request.method == 'POST':
            for key, user_text in request.POST.items():
                if key == 'csrfmiddlewaretoken':
                    continue

                forbidden_keywords = ["<script>", "1==1", "' or '1'='1", "drop table"]
                flagged_word = None

                for words in forbidden_keywords:
                    if words in user_text.lower():
                        flagged_word = words
                        break

                if flagged_word:
                    sec_audit_log.objects.create(
                        attempted_payload=user_text,
                        flagged_keywords=flagged_word,
                        ip_address=ip
                    )

                    user_input.objects.create(
                        text=user_text,
                        is_safe=False
                    )
                    return HttpResponse(f"🔴 SECURITY SHIELD INTERCEPT: Access Denied. Your IP ({ip}) has been logged for system auditing.")
            
        response = self.get_response(request)
        return response
