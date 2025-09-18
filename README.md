# CrowdBolt CrowdVolt Clone

A modern marketplace platform for buying and selling limited edition sneakers, streetwear, and collectibles.

## Architecture

This is a monorepo containing:
- **Frontend**: Next.js with TypeScript, TailwindCSS, Redux Toolkit
- **Backend**: Django REST Framework with PostgreSQL
- **Infrastructure**: Docker containerization

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd CrowdBolt_stockX_clone
   ```

2. **Start with Docker (Recommended)**
   ```bash
   docker-compose up -d
   ```

3. **Or run services separately**

   **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

## Tech Stack

- **Frontend**: Next.js, React, TypeScript, TailwindCSS, Redux Toolkit
- **Backend**: Django, Django REST Framework, PostgreSQL
- **DevOps**: Docker, GitHub Actions
- **Payments**: Stripe Connect

## License

This project is for educational purposes.
