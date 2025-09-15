# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📂 Project Structure (Monorepo)

```
CrowdBolt_stockX_clone/
├── frontend/                 # Next.js React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Next.js page routes
│   │   ├── hooks/          # Custom React hooks (RTK Query)
│   │   ├── store/          # Redux store configuration
│   │   └── styles/         # TailwindCSS styles
│   ├── __tests__/          # Jest + RTL tests
│   └── cypress/            # E2E tests
├── backend/                 # Django REST API
│   ├── apps/               # Django apps
│   │   ├── users/          # User management
│   │   ├── events/         # Event/ticket listings
│   │   ├── transactions/   # Payment processing
│   │   └── reviews/        # User reviews
│   ├── config/             # Django settings
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml       # Multi-service orchestration
├── .github/                 # CI/CD workflows
└── docs/                   # Project documentation
```

### Initial Project Setup
When setting up this project from scratch:

1. **Frontend Setup:**
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --eslint --app
   cd frontend && npm install @reduxjs/toolkit react-redux
   ```

2. **Backend Setup:**
   ```bash
   mkdir backend && cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install django djangorestframework django-cors-headers
   django-admin startproject config .
   ```

3. **Database Setup:**
   ```bash
   # PostgreSQL configuration in Django settings
   # Run migrations after model creation
   python manage.py migrate
   ```

---

## ⚙️ Tech Stack

- **Frontend:** Next.js (React, TypeScript, TailwindCSS)
- **Backend:** Django 5.x, Django REST Framework
- **Database:** PostgreSQL
- **State Management:** Redux Toolkit + RTK Query
- **Payments:** Stripe Connect
- **Testing:** Jest + React Testing Library (frontend), Pytest + DRF test client (backend), Cypress (E2E)
- **Infra:** Docker + docker-compose, CI/CD via GitHub Actions
- **Monitoring:** Sentry (frontend & backend), Prometheus + Grafana (infra)

---

## 🛠️ Development Commands

### Frontend (Next.js)
```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run E2E tests
npm run cypress:open

# Linting and formatting
npm run lint
npm run lint:fix
npm run format
```

### Backend (Django)
```bash
# Start development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python -m pytest
python -m pytest apps/specific_app/tests/

# Code quality
black .
isort .
flake8 .

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Docker Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose up --build
```

---

## 🧠 Project Awareness & Context Rules

- **Parallel Execution Rule:** All tasks (frontend, backend, database, tests) must be built in parallel.
- **Frontend + Backend Concurrency:** Any new feature requires creating UI, API, model, and tests at the same time.
- **Compliance:** GDPR-ready, WCAG 2.1 AA accessibility.
- **Security Baseline:** HTTPS only, JWT with refresh rotation, CSRF tokens, SQL injection protection via ORM.

---

## 🏗 Code Structure Guidelines

### Frontend
- Component-based architecture, colocate component + test + styles.
- Reusable hooks for API calls (RTK Query).
- Page-level routes under `src/pages`.

### Backend
- MVC pattern: `routes/ → controllers/ → models/`.
- DRF serializers for data validation.
- Explicit service layer for marketplace logic.
- Split tests per app (`apps/<app>/tests`).

### Database
- PostgreSQL schema migrations managed via Django migrations.
- Normalize schema: users, events, tickets, transactions, reviews.

---

## 🧪 Testing Requirements

- **Unit Tests:** Components (Jest), Models & Serializers (Pytest).
- **Integration Tests:** API endpoints (DRF test client), frontend API calls (RTL + Mock Service Worker).
- **E2E Tests:** Cypress for full user flows (buy/sell ticket).
- **Performance Tests:** Lighthouse (frontend), Locust (backend).

Testing Pyramid executed **in parallel**:
- Unit → Integration → E2E → Performance.

---

## 🔄 Task Completion Workflow

1. Create GitHub Issue → Assign parallel subtasks:
   - UI Component
   - API Route
   - Database Model/Serializer
   - Tests (frontend + backend)
2. Work in feature branch with parallel commits.
3. PR requires green checks on:
   - Frontend tests
   - Backend tests
   - Integration/E2E tests
4. Merge after approval + automated build success.

---

## 🎨 Style Conventions

- **Frontend:** TypeScript strict mode, ESLint + Prettier, TailwindCSS for styling.
- **Backend:** PEP8, Black formatter, isort, flake8.
- **Commits:** Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`).
- **Docs:** JSDoc for frontend, docstrings for backend.

---

## 📚 Documentation Standards

- **README.md:** High-level overview + setup.
- **claude.md:** Development rules & architecture (this file).
- **API Docs:** Auto-generated OpenAPI (via DRF + drf-spectacular).
- **Component Docs:** Storybook for React components.
- **Runbooks:** Deployment & incident playbooks in `/docs`.

---

## 🔒 Sensitive Data Access Rules

Developers must **never access or hardcode** the following directly in source code:

- **API keys**  
- **Environment variables** (e.g., `.env` values)  
- **Database credentials**  
- **Stripe or payment secrets**  
- **JWT signing keys**  
- **Any personal user data** not explicitly exposed via APIs  

### ✅ Allowed Practice
- Always use `process.env.*` (frontend) or `os.environ.get()` (backend) to reference env vars.
- Store real secrets in **`.env` files** (local only) and use **secret managers** in production.
- Document new env vars in `.env.example`, not in code.

### 🚫 Not Allowed
- No hardcoded tokens, passwords, or API keys in commits.  
- No direct reading/writing to `.env.production` in application code.  
- No pushing real `.env` files to GitHub.  

---


---
