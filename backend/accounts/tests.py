from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import SiteSettings

User = get_user_model()


class AuthSmokeTests(TestCase):
    def test_login_redirects_to_dashboard(self):
        User.objects.create_user(email="user@example.com", password="pass-1234")
        response = self.client.post(
            reverse("login"),
            {"username": "user@example.com", "password": "pass-1234"},
        )
        self.assertRedirects(response, reverse("dashboard"))


class RegistrationToggleTests(TestCase):
    def test_registration_closed_returns_404(self):
        settings = SiteSettings.get_solo()
        settings.registration_enabled = False
        settings.save()

        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 404)

    def test_registration_open_creates_user(self):
        settings = SiteSettings.get_solo()
        settings.registration_enabled = True
        settings.save()

        response = self.client.post(
            reverse("register"),
            {
                "email": "new@example.com",
                "name": "New User",
                "password1": "pass-1234",
                "password2": "pass-1234",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(email="new@example.com").exists())
