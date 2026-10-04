from django.db import models

class user_input(models.Model):
    text = models.TextField()
    is_safe = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id}: {self.text[:30]}..."

class sec_audit_log(models.Model):
    attempted_payload = models.TextField()
    flagged_keywords = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"CRITICAL ALERT [ID {self.id}]: Intercepted '{self.flagged_keywords}'"