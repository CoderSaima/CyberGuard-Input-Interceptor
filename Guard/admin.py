from django.contrib import admin
from .models import user_input, sec_audit_log


@admin.register(user_input)
class AdminUser(admin.ModelAdmin):  
    list_display = ['text', 'is_safe', 'created_at']  
    list_filter = ['is_safe', 'created_at']


@admin.register(sec_audit_log)
class AdminSec(admin.ModelAdmin):  
    list_display = ['attempted_payload', 'flagged_keywords', 'timestamp'] 
    list_filter = ['timestamp']
