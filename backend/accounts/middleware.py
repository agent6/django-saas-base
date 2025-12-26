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
            allowed_views = {
                "force-password-change",
                "logout",
            }
            if current_view not in allowed_views and not request.path_info.startswith("/static/"):
                return redirect("force-password-change")
        return self.get_response(request)
