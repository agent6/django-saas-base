from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("", include("accounts.urls")),
    path("admin/", include("adminpanel.urls")),
]
