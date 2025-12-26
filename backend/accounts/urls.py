from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("force-password-change/", views.force_password_change, name="force-password-change"),
    path("password-change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
    path(
        "password-change/done/",
        views.CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password-reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
