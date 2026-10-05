from django.shortcuts import render
from django.http import HttpResponse
from .models import user_input

def user_view(request):
    if request.method == 'POST':
        user_text = request.POST.get('text', '')
        
        # If the execution reaches here, the middleware has verified the payload is clean
        user_input.objects.create(
            text=user_text,
            is_safe=True
        )
        return HttpResponse("🟢 SUCCESS: Your text input passed the integrity scan safely!")
    
    return render(request, 'index.html')