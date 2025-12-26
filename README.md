# Django SaaS Base

A production-minded starter for Django + HTMX + Tailwind with a custom admin area (no Django admin UI), Brevo SMTP support, and a bootstrap initial admin user.

## Features

- Public pages: home, login, password reset, optional registration
- Authenticated pages: dashboard, profile
- Custom admin area: settings, users, groups
- HTMX-enhanced search for admin lists
- Brevo SMTP support and test email action
- Initial admin user bootstrap via environment variables with forced password reset
- Email-based authentication (no Django admin UI)

## Quick start (Docker)

1. Copy `.env.example` to `.env` and fill in values.
2. Start services:

```bash
docker compose up --build
```

The entrypoint runs migrations and ensures the initial admin user exists. The app is available at `http://localhost:8000` unless you set `HOST_PORT` in `.env`.

Note: local development uses `docker-compose.override.yml` to mount the code into the container. For Portainer or production, the base `docker-compose.yml` intentionally avoids host bind mounts.

Production note: the container runs `gunicorn` by default. For local dev, the override uses Django's `runserver`. Static assets are served with WhiteNoise in production.

## Local setup (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export $(cat .env | xargs)
python backend/manage.py migrate
python backend/manage.py ensure_initial_admin
python backend/manage.py runserver
```

## Environment variables

See [.env.example](.env.example) for the full list. Key values:

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- `DATABASE_URL`
- `INITIAL_ADMIN_EMAIL`, `INITIAL_ADMIN_PASSWORD`, `INITIAL_ADMIN_NAME`
- `INITIAL_ADMIN_FORCE_PASSWORD_RESET` (forces reset at first login)
- `INITIAL_ADMIN_RESET_PASSWORD` (re-apply password on startup if needed)
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

Portainer note: define these values in the stack environment variables so they are injected into the container on deploy.

## Repository hygiene (GitHub-ready)

- `.env` is local-only and must never be committed.
- Use `.env.example` as the safe, shareable template.
- Rotate any credentials that were ever pasted into chat or logs.

## Architecture standards

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the non-negotiable engineering standards.

## Vibe coding workflow

See [docs/VIBE-CODING.md](docs/VIBE-CODING.md) for the repeatable CODEX CLI workflow to start and ship new projects.

## Registration toggle

Registration is controlled by `SiteSettings.registration_enabled` in the Admin settings page. When disabled, the registration route returns a closed message.

## Brevo SMTP

- SMTP host and port are configurable in the Admin settings page.
- SMTP password is **never stored in the database**. It must be set via `EMAIL_HOST_PASSWORD`.
- Use the “Send test email” button to validate configuration.

## Initial admin bootstrap

On startup:

- If no admin exists and `INITIAL_ADMIN_EMAIL`/`INITIAL_ADMIN_PASSWORD` are set, a superuser is created.
- If `INITIAL_ADMIN_FORCE_PASSWORD_RESET=true`, the user is forced to change their password on first login.
- If `INITIAL_ADMIN_RESET_PASSWORD=true`, the admin password is reset on startup using the env vars.

## Deployment notes

- This project intentionally excludes Django admin UI.
- Place the app behind a reverse proxy for TLS termination (e.g., Nginx, Caddy, or Cloudflare Tunnel).
- Configure `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` when running behind HTTPS.
