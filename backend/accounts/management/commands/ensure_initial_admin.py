from django.core.management.base import BaseCommand

from accounts.bootstrap import ensure_initial_admin


class Command(BaseCommand):
    help = "Ensure the initial admin user exists based on environment variables."

    def handle(self, *args, **options):
        ensure_initial_admin(silent_fail=False)
        self.stdout.write(self.style.SUCCESS("Initial admin check complete."))
