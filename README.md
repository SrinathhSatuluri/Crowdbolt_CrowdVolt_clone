# CrowdBolt - CrowdVolt Clone

A marketplace platform for buying and selling EDM and rave event tickets, built with a modern full-stack architecture.

## About
CrowdBolt is an event ticket resale marketplace focused on electronic music events. Users can buy and sell tickets with role-based access control, featuring a responsive design and real-time event discovery.

## Architecture
- **Frontend**: Next.js 15, TypeScript, TailwindCSS, Redux Toolkit
- **Backend**: Django 5.2 REST Framework, SQLite (PostgreSQL ready)
- **Authentication**: JWT with role-based access control
- **Infrastructure**: Docker, Vercel deployment

## Features
- **Role-based System**: Separate buyer and seller capabilities
- **Event Discovery**: Real-time search and filtering
- **Responsive Design**: Mobile-first interface with TailwindCSS
- **Ticket Management**: Secure listing and purchasing workflow
- **Authentication**: JWT-based user management

## Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose

## Quick Start

### 1. Clone Repository
```bash
git clone <repo-url>
cd CrowdBolt_stockX_clone
```

### 2. Start with Docker (Recommended)
```bash
docker-compose up -d
```

### 3. Run Services Separately

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## Project Structure
```
CrowdBolt_stockX_clone/
├── frontend/           # Next.js application
├── backend/           # Django REST API
│   ├── apps/
│   │   ├── users/     # User management
│   │   └── products/  # Event/ticket management
├── docker-compose.yml
└── README.md
```

## Development Status
- User authentication system
- Role-based access control
- Responsive frontend interface
- Event browsing and search
- Ticket purchasing workflow (in progress)
- Payment integration (in progress)
- PostgreSQL migration (in progress)