from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from .bootstrap import ensure_initial_admin

        ensure_initial_admin(silent_fail=True)
