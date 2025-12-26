from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminPermissionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass-1234")
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="pass-1234",
            is_staff=True,
        )

    def test_admin_settings_requires_staff(self):
        self.client.login(email="user@example.com", password="pass-1234")
        response = self.client.get(reverse("admin-settings"))
        self.assertEqual(response.status_code, 403)

    def test_admin_settings_allows_staff(self):
        self.client.login(email="admin@example.com", password="pass-1234")
        response = self.client.get(reverse("admin-settings"))
        self.assertEqual(response.status_code, 200)
