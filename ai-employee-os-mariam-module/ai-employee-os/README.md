# AI Employee OS — Member 6 module (Mariam Osama)

Scope: **Frontend, Backend, Security & Infrastructure**. This is only this module —
the other five members' parts (AI Brain, Communication, CRM, Finance, Documents/Reporting)
are not included here and are expected to plug into the `/api/*` surface this backend exposes.

## Structure

```
ai-employee-os/
├── backend/                 FastAPI service
│   ├── app/
│   │   ├── core/            config, JWT + password hashing, MFA (TOTP), auth dependency
│   │   ├── db/               SQLAlchemy async engine + models (Organization, User)
│   │   ├── api/               auth.py (register/login/MFA/refresh), pricing.py (plans/usage/upgrade)
│   │   └── schemas/          Pydantic request/response models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                 Next.js 14 (App Router) + TypeScript + Tailwind
│   ├── app/                   /, /login, /login/mfa, /register, /dashboard
│   ├── components/           UsageMeter
│   ├── lib/api.ts             typed fetch client
│   └── Dockerfile
└── docker-compose.yml        postgres + redis + backend + frontend
```

## What's implemented

**Authentication & security**
- Email/password registration and login (bcrypt via passlib)
- JWT access + refresh tokens
- TOTP-based MFA (`pyotp`) — enable per user, verified on login
- Role field (`owner` / `admin` / `member`) + `require_role()` dependency for
  department-based permission checks (the Business-plan "Department-based Permissions" feature)

**Database**
- Async PostgreSQL via SQLAlchemy 2.0 (`asyncpg`)
- `Organization` (tenant) and `User` models; each org has a `plan_tier`

**Pricing plans (Business Features)**
- `PLAN_LIMITS` encodes the Basic/Pro/Business limits from the spec (seats, AI
  requests, storage)
- `GET /api/pricing/plans` — public pricing table
- `GET /api/pricing/usage` — an org's current usage vs. its plan limit
- `enforce_ai_request_quota` — a dependency other members can attach to any
  AI-employee endpoint (e.g. AI Sales Manager) to enforce Fair Use limits and
  return `402 Payment Required` once exhausted
- `POST /api/pricing/upgrade` — owner/admin only

**Frontend**
- Landing page, login (+ MFA step), register, and a dashboard shell reading
  live plan usage from the backend
- Custom Tailwind token system (`tailwind.config.ts`) — deep navy/graphite
  console with a single amber signal color, not a generic template palette
- JWT stored in a client cookie via `lib/api.ts`; swap for httpOnly cookies
  issued server-side before production

## Running it locally

```bash
cp backend/.env.example backend/.env   # then edit SECRET_KEY
docker compose up --build
```

- Backend: http://localhost:8000 (docs at `/docs`)
- Frontend: http://localhost:3000

Or run each service natively:

```bash
# backend
cd backend
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend
cd frontend
npm install
npm run dev
```

## Not in this module (owned by teammates)

AI brain/routing (Ammar), email/WhatsApp/meetings (Hafiz), CRM (Fouzia),
quotations/invoices (Manahil), document intelligence/reporting (Abdullah).
This backend's `/api/auth` and `/api/pricing` routes, plus the `User`/
`Organization` tables, are the shared foundation those modules should build on.

## Next steps for this module

- Alembic migrations instead of `create_all` on startup
- Redis-backed session/rate-limit layer for the auth endpoints
- Kubernetes manifests (Deployment/Service/Ingress) once the API is stable
- SSO (Business plan) — wire Auth.js on the frontend against an OIDC provider
