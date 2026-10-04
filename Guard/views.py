from django.shortcuts import render
from django.http import HttpResponse
from .models import sec_audit_log, user_input

def user_view(request):
    if request.method == 'POST':
        user_text = request.POST.get('text', '')

        forbidden_keywords = ["<script>", "1==1", "' or '1'='1", "drop table"]
        flagged_words = None

        for words in forbidden_keywords:
            if words in user_text.lower():
                flagged_words = words
                break

        if flagged_words:
            sec_audit_log.objects.create(
                attempted_payload=user_text,
                flagged_keywords=flagged_words
            )
            user_input.objects.create(
                text=user_text,
                is_safe=False
            )
            return HttpResponse("🔴 SECURITY ALERT: Malicious entry intercepted and logged!")
        else:
            user_input.objects.create(
                text=user_text,
                is_safe=True
            )
            return HttpResponse("🟢 SUCCESS: Your text input passed the integrity scan safely!")
    
    return render(request, 'index.html')
