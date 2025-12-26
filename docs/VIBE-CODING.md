# VIBE-CODING.md

**Building Products on `django-saas-base` with OpenAI CODEX CLI**

---

## Purpose

This document defines a **repeatable, disciplined workflow** for building real production applications on top of **`django-saas-base`** using the **OpenAI CODEX CLI**.

The goal is to:

- Move fast without breaking fundamentals
- Use AI to accelerate *implementation*, not *decision-making*
- Maintain clean architecture, UX quality, and long-term maintainability
- Support easy local development and clean production deployment

This process is intentionally **boring, explicit, and iterative** -- because that's how good software gets built.

---

## Terminology Standard (Important)

To avoid ambiguity and keep documentation, prompts, and implementation aligned, this project uses the following terminology consistently:

- **Pages** -> User-facing units mapped to URLs (planning & UX term)
- **Views** -> Django view functions/classes (implementation detail)
- **Templates** -> HTML files rendered by Django
- **Partials** -> HTMX fragments rendered server-side

> **Always use "Pages"** in planning documents, user stories, tasks, and CODEX prompts.

---

## Local Development Environment (Baseline)

### Hardware & OS

- macOS (primary)
- Same workflow works on Windows or Linux

### Tools

- **VS Code**
- **VS Code Terminal**
- **OpenAI CODEX CLI**
- **Docker Desktop**
- **GitHub**

### Typical VS Code Setup

- **Terminal Tab 1:** CODEX CLI (prompting + implementation)
- **Terminal Tab 2:** Shell access
  - `docker compose up --build -d`
  - `docker compose logs`
  - `pytest`, `ruff`, etc.
- **Docker Desktop:**
  - Monitor container health
  - Inspect logs
  - Restart services when needed

### Philosophy

- Local dev environment is **disposable**
- You should be able to:
  - Stop everything
  - Delete containers
  - Rebuild from scratch
- If you *can't* do that easily, the project is already in trouble

---

## Creating a New Project from `django-saas-base`

### Step 1: Create a New GitHub Repository

- Use **`django-saas-base`** as a **template**
- Name the new repo after the actual product (not "test" or "demo")
- Clone it locally

Example:

```
git clone git@github.com:your-org/my-new-product.git
cd my-new-product
```

---

## Step 2: Define the Project (Before Writing Code)

### Project Definition (Required)

Write this down **before** prompting CODEX:

- What problem does this product solve?
- Who is it for?
- Is it internal, customer-facing, or both?
- Is it multi-tenant or single-tenant?
- Any compliance/security concerns?

Create or update: [docs/PROJECT.md](PROJECT.md)

This document is **the source of truth**.
CODEX does not decide product scope -- *you do*.

---

## Step 3: Define User Types

Before Pages or features, define **who exists in the system**.

Examples:

- Anonymous visitor
- Authenticated user
- Admin
- Manager
- Support agent
- External collaborator

Document:

- What each user type can do
- What they *cannot* do

Add this to: [docs/PROJECT.md](PROJECT.md)

---

## Step 4: Define Pages

Create a **flat list of Pages**:

- Public Pages
- Authenticated Pages
- Admin Pages

For each Page, define:

- Purpose
- Who can access it
- URL
- Primary actions

WARNING: **Mandatory Review Rule**
If AI helps generate this list, **you must read and edit every Page definition before implementing anything**.

Add this to: [docs/PROJECT.md](PROJECT.md)

---

## Step 5: Write User Stories (Per Page)

For **each Page**, define user stories.

Good user stories:

- Are specific
- Are testable
- Are small enough to implement incrementally

Example format:

- "As a ___, I can ___ so that ___."

WARNING: **Mandatory Review Rule**
If AI helps write user stories, **you must review and edit every one**.

User stories define behavior -- sloppy stories create sloppy systems.

---

## Step 6: Convert User Stories into Dev Tasks

For each user story:

- Break it into **implementation tasks**
- Each task must have a **Definition of Done**

### Definition of Done (Required)

A task is done when:

- Feature works as described
- Access control enforced
- Errors handled gracefully
- UX follows the [StyleGuide.md](../StyleGuide.md)
- Tests added if appropriate
- Manual verification completed

Document tasks in: [docs/DEV_TASKS.md](DEV_TASKS.md)

---

## Step 7: CODEX-Driven Implementation Loop (Core Workflow)

This is the **Vibe Coding Loop**.

---

### 1. Create the Page First

For each Page:

- Prompt CODEX to:
  - Create the route
  - Create the Django view
  - Create the template
  - Add basic layout and navigation
- Ensure the Page renders successfully in the browser

This gives you **a real, visible surface** to iterate on.

---

### 2. Implement One Task at a Time

For each task:

- Paste the task **and its Definition of Done** into the CODEX prompt
- Be explicit about:
  - Files to modify
  - Constraints (no Django admin, HTMX-only, Tailwind, etc.)

**Never batch multiple tasks into a single CODEX prompt.**

---

### 3. Test and Validate

After CODEX completes:

- Reload the Page
- Click through the full flow
- Test unhappy paths
- Check mobile layout
- Review code changes manually

If something feels wrong:

- Fix it manually **or**
- Re-prompt CODEX with corrections

---

### 4. Commit Early and Often

Each completed task = one commit.

Good commits:

- Small
- Descriptive
- Easy to revert

Example:

```
git commit -m "Add profile page email update validation"
```

---

### 5. Repeat

Continue:

- Task -> CODEX -> Test -> Commit

Until the Page is complete, then move to the next Page.

---

## Step 8: Preparing for Production

### Infrastructure Assumptions

- You already have:
  - A server running **Portainer**
  - A **Cloudflare Tunnel** container
- SSL and public access handled by Cloudflare Zero Trust
- App runs HTTP internally only

---

## Step 9: Production Deployment Workflow

### 1. Portainer Setup

- Add a new stack
- Point it at the GitHub repository
- Configure:
  - Environment variables
  - Volumes if required

---

### 2. Start the Application

- Portainer pulls the repo
- Containers build and start
- App is live on the internal Docker network

---

### 3. Cloudflare Tunnel Integration

- Attach the app container to the **same Docker network** as the Cloudflare Tunnel
- In Cloudflare Zero Trust:
  - Edit the tunnel
  - Add a **Published Application Route**
  - Set:
    - Subdomain
    - Internal container IP and port

At this point:

- App is publicly accessible
- SSL is terminated by Cloudflare
- No inbound ports are exposed on the server
- Zero Trust policies can be layered on top

---

## Best Practices (Non-Negotiable)

### AI Usage

- AI writes code
- **You own the architecture**
- **You review everything**
- Never blindly merge AI output

### Code Quality

- Prefer clarity over cleverness
- Explicit is better than implicit
- Repetition is acceptable early
- Abstractions are earned, not assumed

### UX

- Follow the [StyleGuide.md](../StyleGuide.md)
- Mobile-first always
- Admin UX matters as much as user UX

### Security

- No secrets in git
- Environment variables only
- Principle of least privilege
- Never trust user input

---

## Final Philosophy

> **Vibe Coding is not letting AI drive.
> It's letting AI handle the boring parts while you stay responsible for the product.**

If you follow this document:

- You can build fast
- You can stop and restart anytime
- You can onboard new developers easily
- You can ship confidently to production

---
