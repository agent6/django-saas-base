from django import forms
from django.contrib.auth.models import Group

from core.forms import apply_tailwind_classes
from core.models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
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


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)
