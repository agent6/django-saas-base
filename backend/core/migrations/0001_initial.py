from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("registration_enabled", models.BooleanField(default=False)),
                ("email_from_name", models.CharField(blank=True, max_length=150)),
                ("email_from_email", models.EmailField(blank=True, max_length=254)),
                ("email_host", models.CharField(blank=True, max_length=255)),
                ("email_port", models.PositiveIntegerField(default=587)),
                ("email_host_user", models.CharField(blank=True, max_length=255)),
                ("email_use_tls", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
