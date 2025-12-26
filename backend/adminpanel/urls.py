from django.urls import path

from . import views

urlpatterns = [
    path("", views.settings_view, name="admin-home"),
    path("settings/", views.settings_view, name="admin-settings"),
    path("users/", views.user_list, name="admin-users"),
    path("users/new/", views.user_create, name="admin-user-new"),
    path("users/<int:user_id>/", views.user_edit, name="admin-user-edit"),
    path("users/<int:user_id>/reset-password/", views.user_reset_password, name="admin-user-reset"),
    path("groups/", views.group_list, name="admin-groups"),
    path("groups/new/", views.group_edit, name="admin-group-new"),
    path("groups/<int:group_id>/", views.group_edit, name="admin-group-edit"),
]
