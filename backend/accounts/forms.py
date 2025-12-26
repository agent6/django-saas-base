from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.email_utils import get_email_connection, resolve_from_email
from core.forms import apply_tailwind_classes
from core.models import SiteSettings

User = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.input_type = "email"


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)


class AdminUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ["email", "name", "is_active", "is_staff", "groups"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)
        self.fields["is_active"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"
        self.fields["is_staff"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"


class AdminUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ["email", "name", "is_active", "is_staff", "must_change_password", "groups"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)
        self.fields["is_active"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"
        self.fields["is_staff"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"
        self.fields["must_change_password"].widget.attrs[
            "class"
        ] = "h-4 w-4 rounded border-slate-300 text-slate-700"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class TailwindPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)


class SitePasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_tailwind_classes(self)

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(
            subject,
            body,
            from_email,
            [to_email],
            connection=get_email_connection(SiteSettings.get_solo()),
        )
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")
        email_message.send()

    def save(
        self,
        domain_override=None,
        subject_template_name=None,
        email_template_name=None,
        use_https=False,
        token_generator=None,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        site_settings = SiteSettings.get_solo()
        from_email = from_email or resolve_from_email(site_settings)
        return super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            extra_email_context=extra_email_context,
        )
