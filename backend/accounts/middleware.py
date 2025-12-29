from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class MustChangePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.must_change_password:
            try:
                current_view = resolve(request.path_info).view_name
            except Exception:
                current_view = ""

            force_change_url_name = getattr(settings, "FORCE_PASSWORD_CHANGE_URL_NAME", "force-password-change")
            allowed_views = {
                force_change_url_name,
                "logout",
            }

            if current_view not in allowed_views and not request.path_info.startswith("/static/"):
                return redirect(force_change_url_name)
        return self.get_response(request)
