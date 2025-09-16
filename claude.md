# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🏗️ **CrowdBolt Architecture Overview**

**Project Type:** Event ticket resale marketplace (StockX model for events/raves)
**Architecture:** Monorepo with microservice-ready Django apps + Next.js frontend

### **Current Tech Stack**
- **Frontend:** Next.js 15 + TypeScript + TailwindCSS + Redux Toolkit
- **Backend:** Django 5.2 + DRF + PostgreSQL + JWT Authentication
- **Infrastructure:** Docker Compose + Redis (planned)
- **Authentication:** JWT with refresh tokens, role-based access control

## 🛠️ **Development Commands**

### **Start Development Environment**
```bash
# Full stack (recommended)
docker-compose up -d

# Individual services for debugging
# Frontend only
cd frontend && npm run dev

# Backend only (activate venv first)
cd backend && . venv/Scripts/activate && python manage.py runserver

# Database only
docker-compose up db -d
```

### **Frontend Commands**
```bash
cd frontend

# Development
npm run dev          # Start with Turbopack
npm run build        # Production build with Turbopack
npm start           # Start production server
npm run lint        # ESLint check
```

### **Backend Commands**
```bash
cd backend && . venv/Scripts/activate

# Development
python manage.py runserver
python manage.py runserver 0.0.0.0:8000  # Bind to all interfaces

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py dbshell

# Utilities
python manage.py shell
python manage.py collectstatic
python manage.py check --deploy  # Production readiness check
```

### **Docker Commands**
```bash
# Build and start all services
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in containers
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py shell

# Clean up
docker-compose down
docker-compose down -v  # Remove volumes too
```

## 📂 **Project Structure**

```
CrowdBolt_stockX_clone/
├── frontend/                    # Next.js 15 frontend
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   ├── components/         # React components
│   │   ├── hooks/              # Custom hooks (Redux typed)
│   │   ├── providers/          # Context providers
│   │   ├── store/              # Redux Toolkit store
│   │   └── types/              # TypeScript definitions
│   ├── Dockerfile
│   └── package.json            # Dependencies include auth, forms, validation
├── backend/                     # Django 5.2 backend
│   ├── apps/                   # Microservice-style apps
│   │   ├── users/              # Authentication & user management
│   │   └── products/           # Event/ticket management
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Environment-based config
│   │   └── urls.py
│   ├── requirements.txt        # Includes JWT, rate limiting, Argon2
│   └── Dockerfile
├── docker-compose.yml          # Multi-service orchestration
└── README.md
```

## 🔑 **Authentication Architecture**

**Current Implementation:** JWT-based authentication with role-based access control

### **Backend (Django)**
- Custom User model with roles (buyer/seller/admin)
- JWT tokens with short expiration + refresh mechanism
- Rate limiting on auth endpoints
- Argon2 password hashing
- Email verification system (planned)

### **Frontend (Next.js)**
- Redux auth slice with RTK Query
- Typed hooks for auth state management
- Protected route components
- Form validation with react-hook-form + zod

## 🗄️ **Database Schema**

**Database:** PostgreSQL (configured, using SQLite in development)

### **User Model** (apps/users/models.py)
```python
# Extended from AbstractUser
- email (unique, used as username)
- role (buyer/seller/admin)
- is_verified (email verification)
- identity_verified (KYC for fraud prevention)
- failed_login_attempts (security)
```

## 🔒 **Security Configuration**

### **Environment Variables** (.env.example template provided)
```bash
# Django
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

# Database
POSTGRES_DB=crowdbolt_db
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=

# JWT & Auth
JWT_SECRET_KEY=
JWT_ACCESS_TOKEN_LIFETIME=15m
JWT_REFRESH_TOKEN_LIFETIME=7d
```

### **Security Features Implemented**
- CORS configured for frontend origin
- Rate limiting middleware
- Secure JWT configuration
- Environment-based settings
- SQL injection protection via ORM


## 🚀 **Development Workflow**

### **Branch Strategy**
- `main` - Production ready code
- `feature/feature-name` - Feature development
- `hotfix/issue-description` - Critical fixes

### **Commit Convention**
```bash
feat: add user authentication system
fix: resolve JWT token expiration issue
docs: update API documentation
```

## 📝 **API Documentation**

**Backend API Endpoints** (Django REST Framework)
- Auto-generated OpenAPI docs at `/api/docs/` (when configured)
- Current base URL: `http://localhost:8000/api/`

**Frontend API Integration**
- RTK Query for data fetching
- Typed API hooks in `src/hooks/`
- Axios configured with interceptors

## 🐳 **Docker Development**

**Services:**
- `frontend` - Next.js development server (port 3000)
- `backend` - Django development server (port 8000)
- `db` - PostgreSQL database (port 5432)

**Volumes:**
- Source code mounted for live reloading
- Database persistence with named volume

## 💡 **Key Development Principles**

### **MVP-First Approach**
- Ship fast, iterate quickly
- Focus on core features first
- Use proven patterns and libraries
- Minimal viable security without over-engineering

### **Code Quality Standards**
- **Frontend:** TypeScript strict mode, ESLint + Prettier
- **Backend:** PEP8, Black formatter, isort, flake8
- **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`)

### **Security Guidelines**
- Environment variables only (no hardcoded secrets)
- JWT token security with proper expiration
- Input validation on all endpoints
- Rate limiting on authentication endpoints

## 📋 **Common Issues & Solutions**

### **Docker Issues**
```bash
# Container port conflicts
docker-compose down && docker-compose up -d

# Database connection issues
docker-compose exec backend python manage.py dbshell

# Frontend build issues
docker-compose build --no-cache frontend
```

### **Development Setup**
```bash
# Backend virtual environment issues
cd backend && python -m venv venv && . venv/Scripts/activate
pip install -r requirements.txt

# Node modules issues
cd frontend && rm -rf node_modules && npm install
```

---

**Next Steps:** Currently implementing User Authentication microservice with JWT tokens and role-based access control.
