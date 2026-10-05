from django.db import models

class user_input(models.Model):
    text = models.TextField()
    is_safe = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cyberguard_user_input'
        verbose_name = 'User Input'
        verbose_name_plural = 'User Inputs'

    def __str__(self):
        return f"Submission {self.id}: {self.text[:30]}..."

class sec_audit_log(models.Model):
    attempted_payload = models.TextField()
    flagged_keywords = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'cyberguard_security_log'
        verbose_name = 'Security Audit Log'
        verbose_name_plural = 'Security Audit Logs'

    def __str__(self):
         return f"CRITICAL [ID {self.id}]: Intercepted '{self.flagged_keywords}' from {self.ip_address}"