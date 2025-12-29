from django.conf import settings
from django.core.mail import EmailMessage, get_connection


def resolve_from_email(site_settings):
    from_email = site_settings.email_from_email or settings.DEFAULT_FROM_EMAIL
    if site_settings.email_from_name:
        return f"{site_settings.email_from_name} <{from_email}>"
    return from_email


def get_email_connection(site_settings, password_override=None):
    password = password_override or settings.EMAIL_HOST_PASSWORD
    if site_settings.email_host:
        host = site_settings.email_host
        port = site_settings.email_port
        host_user = site_settings.email_host_user or settings.EMAIL_HOST_USER
        use_tls = site_settings.email_use_tls
        if site_settings.email_host_password:
            password = password_override or site_settings.email_host_password
    else:
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        host_user = settings.EMAIL_HOST_USER
        use_tls = settings.EMAIL_USE_TLS

    return get_connection(
        host=host,
        port=port,
        username=host_user,
        password=password,
        use_tls=use_tls,
    )


def send_test_email(site_settings, to_email, password_override=None):
    subject = "Email configuration test"
    body = "This is a test email sent from your Django starter app."
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=resolve_from_email(site_settings),
        to=[to_email],
        connection=get_email_connection(site_settings, password_override=password_override),
    )
    email.send(fail_silently=False)
