# Architecture Standards

This document defines the non-negotiable engineering standards for this project.
These rules must be followed for all future changes.

## Non-Negotiables

1. **No Django admin site**
   - The Django admin app is not installed.
   - No `/admin/` URLs from Django admin are exposed.

2. **Server-rendered HTML**
   - Django templates are the source of truth for HTML.
   - HTMX is used for partial updates and progressive enhancement.

3. **Tailwind**
   - UI uses Tailwind classes with consistent tokens and component patterns.
   - Avoid ad-hoc styling or inline styles outside the system.

4. **12-factor configuration**
   - All configuration via environment variables.
   - Secrets are never stored in the database.

5. **Postgres in Docker**
   - Postgres is the recommended local/dev database using Docker.
   - Compose should include a Postgres service for realistic SaaS parity.

6. **Authentication**
   - Session-based auth only.
   - Password reset via email.
   - Registration is controlled by a DB setting (toggleable in admin settings).

7. **Initial admin bootstrap**
   - Initial admin created from env vars on first startup.
   - Forced password reset on first login for that admin.

## HTMX Interaction Standards

These interaction patterns are required to keep UX consistent.

### List Pages (Users/Groups)

- Search input triggers an HTMX request that updates the list region only.
- Pagination links trigger HTMX updates to the list region.

### Edit Pages

- Standard full-page edit forms (simple, predictable).
- Optional "Save" submits the form normally (no HTMX required).
- Validation errors must render inline with the form fields.

### Flash Messages

- Use consistent toast/banner styling across the app.

## Quality Gates

These gates keep the repo production-ready from day one.

### Formatting and Linting

- Use `black` for formatting and `ruff` for linting.
- Run `black` and `ruff` before merging changes.

### Tests

- Maintain minimal smoke tests for:
  - Authentication flows
  - Admin permissions
  - Registration toggle behavior

### Security Basics

- CSRF protection is required for all POST/HTMX forms.
- Secure cookies must be configurable for reverse proxy deployments.
  - `SESSION_COOKIE_SECURE`
  - `CSRF_COOKIE_SECURE`
