# Application Style Guide

**Modern, Professional, Admin-Friendly Web App**

## 1. Product Personality & Design Principles

### Brand Personality

- **Professional** - suitable for internal tools and client-facing portals
- **Calm & trustworthy** - nothing flashy or experimental
- **Efficient** - optimized for frequent admin use
- **Neutral** - adaptable to future branding

### Core Principles

1. **Content First** - UI never overshadows data
2. **Predictability** - patterns repeat everywhere
3. **Progressive Disclosure** - show complexity only when needed
4. **Accessibility by Default** - readable, keyboard-friendly, screen-reader aware
5. **HTMX-Compatible** - interactions degrade gracefully without JS

## 2. Layout System




### Global Page Structure

- **Header (Top Bar)**
  - Logo / App Name (left)
  - User menu (right)
- **Main Content Area**
- **Footer (minimal)**
  - Optional copyright / version

### Admin Pages

- Use **content-centered layout**
- Avoid heavy sidebars initially
- Admin navigation appears as:
  - Top-level tabs
  - Or contextual navigation within admin pages

### Max Content Width

- Desktop: `max-w-7xl`
- Forms: `max-w-2xl`
- Lists/tables: full width

## 3. Color System




### Base Palette

- **Primary:** Slate / Blue-gray
- **Accent:** Indigo or Blue
- **Success:** Green
- **Warning:** Amber
- **Error:** Red
- **Background:** Near-white / light gray

### Color Usage Rules

- Primary color = actions and links
- Accent color = focus, highlights
- Never rely on color alone to convey meaning
- Avoid pure black; use dark gray instead

### Example Semantic Roles

- Primary Action: solid accent color
- Secondary Action: neutral outline
- Destructive Action: red, always confirmed

## 4. Typography




### Font Choice

- **System UI font stack**
  - Fast
  - Accessible
  - Consistent across OSes

### Type Scale

- Page title
- Section header
- Body text
- Small/meta text
- Labels

### Typography Rules

- Sentence case everywhere
- Avoid ALL CAPS except badges
- Line length: 60-75 characters max
- Left-aligned text only

## 5. Spacing & Rhythm

### Spacing Philosophy

- Consistent vertical rhythm
- White space is intentional, not empty

### Layout Spacing

- Page padding: generous on desktop, compact on mobile
- Section separation: visible but subtle
- Forms: clear grouping, not cramped

## 6. Buttons & Actions




### Button Hierarchy

1. **Primary**
   - One per view maximum
2. **Secondary**
   - Supporting actions
3. **Tertiary / Link**
   - Low-emphasis actions
4. **Destructive**
   - Always visually distinct

### Button Rules

- Verbs first: "Save changes", "Create user"
- No icons-only buttons without labels (except known patterns)
- Disabled buttons explain *why* when possible

## 7. Forms & Inputs




### Form Layout

- One column by default
- Logical field grouping
- Labels above inputs
- Inline help text under inputs

### Validation

- Real-time when possible
- Error messages:
  - Specific
  - Human-readable
  - Never technical

### Required Fields

- Mark clearly
- Avoid `*` alone; pair with text

## 8. Tables, Lists & Data Views




### Tables

- Used for admin lists (users, groups)
- Zebra striping optional
- Sticky headers on long lists
- Clickable rows only when predictable

### Mobile Behavior

- Convert rows into stacked cards
- Hide non-essential columns
- Preserve primary identifier first

## 9. Navigation & Information Architecture

### Public Navigation

- Home
- Login
- Register (if enabled)

### Authenticated Navigation

- Dashboard
- Profile
- Admin (if admin)

### Admin Navigation

- Settings
- Users
- Groups

Rules:

- No more than 2 levels deep
- Navigation labels match page titles exactly

## 10. HTMX Interaction Patterns




### Preferred Patterns

- Inline save forms
- Modal dialogs for edits
- Partial refresh for lists
- Toast-style confirmation messages

### UX Rules

- Always show loading state
- Always show success or error feedback
- Never silently fail
- HTMX actions must be reversible when possible

## 11. Feedback & System States

### Success

- Subtle green confirmation
- Auto-dismiss after short time

### Errors

- Red, human-readable
- Near the source of the problem

### Empty States

- Explain what this means
- Explain what to do next
- Never leave blank screens

## 12. Authentication UX

### Login

- Minimal distractions
- Clear error messages
- Password visibility toggle (recommended)

### Password Reset

- Reassuring copy
- Security-neutral messaging
- Clear next steps

### First Login Password Reset (Admin)

- Mandatory
- Cannot be skipped
- Clear explanation why

## 13. Accessibility Standards

### Required Practices

- WCAG AA contrast minimums
- Keyboard navigation
- Visible focus states
- Screen reader-friendly labels
- Click targets >= 44px on mobile

### Non-Negotiables

- No color-only meaning
- No hover-only actions
- No hidden critical UI behind icons alone

## 14. Mobile Experience




### Mobile-First Rules

- Forms optimized for thumbs
- Tables collapse into cards
- Buttons full-width where appropriate
- Avoid hover-dependent UI

## 15. Tone & Microcopy

### Voice

- Clear
- Calm
- Neutral
- Helpful

### Examples

- Bad: "Invalid input"
- Good: "Please enter a valid email address"
- Bad: "Error 403"
- Good: "You don't have permission to access this page."

## 16. What This Style Guide Enables

- Fast onboarding for new contributors
- Consistent UI across future projects
- Easier refactors and redesigns
- Clear separation of UX intent from implementation
- Professional appearance suitable for internal tools or SaaS

---

If you want, next steps could include:

- A **design token table** (colors, spacing, typography mapped to Tailwind)
- A **page-by-page wireframe description**
- A **UI checklist** for PR reviews
- A **light/dark mode extension** of this guide

Just tell me how far you want to take it.
