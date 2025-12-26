from email.utils import parseaddr

from django import forms
from django.conf import settings as django_settings
from django.contrib.auth.models import Group

from core.forms import apply_tailwind_classes
from core.models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    email_host_password = forms.CharField(
        label="SMTP password",
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter new to change"}, render_value=False),
        help_text="Managed via environment variable. Enter a value to test without saving.",
    )

    class Meta:
        model = SiteSettings
        fields = [
            "registration_enabled",
            "email_from_name",
            "email_from_email",
            "email_host",
            "email_port",
            "email_host_user",
            "email_use_tls",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)
        self.fields["registration_enabled"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"
        self.fields["email_use_tls"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"
        self.fields["email_host_password"].widget.attrs[
            "class"
        ] = "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-500"
        name, email = parseaddr(django_settings.DEFAULT_FROM_EMAIL)
        env_initials = {
            "email_from_name": name or "",
            "email_from_email": email or "",
            "email_host": django_settings.EMAIL_HOST,
            "email_port": django_settings.EMAIL_PORT,
            "email_host_user": django_settings.EMAIL_HOST_USER,
            "email_use_tls": django_settings.EMAIL_USE_TLS,
        }
        for field_name, value in env_initials.items():
            self.initial[field_name] = value


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)
