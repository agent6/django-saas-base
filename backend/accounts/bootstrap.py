import os

from django.db.utils import OperationalError, ProgrammingError

from .models import User


def _env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() == "true"


def ensure_initial_admin(silent_fail=False):
    email = os.getenv("INITIAL_ADMIN_EMAIL")
    password = os.getenv("INITIAL_ADMIN_PASSWORD")
    name = os.getenv("INITIAL_ADMIN_NAME", "")
    if not email or not password:
        return

    force_reset = _env_bool("INITIAL_ADMIN_FORCE_PASSWORD_RESET", True)
    reset_existing = _env_bool("INITIAL_ADMIN_RESET_PASSWORD", False)

    try:
        admin_exists = User.objects.filter(is_staff=True, is_active=True).exists()
    except (OperationalError, ProgrammingError):
        if silent_fail:
            return
        raise

    if not admin_exists:
        User.objects.create_superuser(
            email=email,
            password=password,
            name=name,
            must_change_password=force_reset,
        )
        return

    if reset_existing:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
        user.set_password(password)
        if force_reset:
            user.must_change_password = True
        user.is_active = True
        user.save(update_fields=["password", "must_change_password", "is_active"])
