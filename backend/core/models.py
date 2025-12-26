from django.db import models


class SiteSettings(models.Model):
    registration_enabled = models.BooleanField(default=False)
    email_from_name = models.CharField(max_length=150, blank=True)
    email_from_email = models.EmailField(blank=True)
    email_host = models.CharField(max_length=255, blank=True)
    email_port = models.PositiveIntegerField(default=587)
    email_host_user = models.CharField(max_length=255, blank=True)
    email_use_tls = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Settings"

    @classmethod
    def get_solo(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings
