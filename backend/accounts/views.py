from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from core.models import SiteSettings

from .forms import (
    LoginForm,
    ProfileForm,
    RegistrationForm,
    SitePasswordResetForm,
    TailwindPasswordChangeForm,
)


class CustomLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.must_change_password:
            return redirect("force-password-change")
        return response


class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("home")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


def register(request):
    settings = SiteSettings.get_solo()
    if not settings.registration_enabled:
        return render(request, "accounts/registration_closed.html", status=404)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def force_password_change(request):
    if not request.user.must_change_password:
        return redirect("dashboard")

    if request.method == "POST":
        form = TailwindPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.must_change_password = False
            request.user.save(update_fields=["must_change_password"])
            messages.success(request, "Password updated. Please log in again.")
            logout(request)
            return redirect("login")
    else:
        form = TailwindPasswordChangeForm(user=request.user)

    return render(request, "accounts/force_password_change.html", {"form": form})


class CustomPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = TailwindPasswordChangeForm
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.must_change_password:
            self.request.user.must_change_password = False
            self.request.user.save(update_fields=["must_change_password"])
        return response


class CustomPasswordChangeDoneView(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    form_class = SitePasswordResetForm


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
