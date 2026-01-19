# Taskie - Multi-User Task Management App

A modern web application for managing tasks with priorities, built with Next.js, FastAPI, and PostgreSQL.

## Features

- **User Authentication** - Sign up, sign in, sign out with JWT tokens
- **Task Management** - Create, read, update, delete tasks
- **Task Priorities** - Organize tasks by low, medium, high priority
- **Task Status** - Mark tasks as complete or incomplete
- **Responsive UI** - Works seamlessly on desktop and mobile
- **Real-time Updates** - Optimistic UI updates with server synchronization

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16+, React 19, TypeScript, Tailwind CSS |
| Backend | Python FastAPI, SQLModel ORM |
| Database | PostgreSQL (Neon Serverless) |
| Authentication | Better Auth with JWT |
| Icons | lucide-react |

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- PostgreSQL connection string (Neon)

### Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with DATABASE_URL and BETTER_AUTH_SECRET
python main.py
# Runs on http://localhost:8001
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with NEXT_PUBLIC_API_BASE_URL
npm run dev
# Runs on http://localhost:3000
```

## Project Structure

```
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/          # Pages and layouts
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities, hooks, API client
│   └── package.json
├── backend/               # FastAPI application
│   ├── src/
│   │   ├── api/          # API endpoints
│   │   ├── auth/         # Authentication logic
│   │   ├── models.py     # Database models
│   │   └── schemas.py    # Request/response schemas
│   ├── main.py
│   └── requirements.txt
├── specs/                 # Feature specifications
└── README.md
```

## API Endpoints

**Authentication:**
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Login user
- `POST /auth/signout` - Logout user

**Tasks:**
- `GET /api/{userId}/tasks` - List all tasks
- `POST /api/{userId}/tasks` - Create task
- `PUT /api/{userId}/tasks/{taskId}` - Update task
- `PATCH /api/{userId}/tasks/{taskId}/status` - Update task status
- `DELETE /api/{userId}/tasks/{taskId}` - Delete task

## Environment Variables

**Backend (.env):**
```
DATABASE_URL=postgresql://user:password@host/db
BETTER_AUTH_SECRET=your_secret_key_min_32_chars
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

## Development

- **Spec-Driven Development** - All features defined in `specs/` before implementation
- **Type Safety** - TypeScript throughout frontend and backend schemas
- **Testing** - Run `npm run build` (frontend) to verify production build
- **Git Workflow** - Feature branches merged to main after code review

## Deployment

**Frontend:** Deploy `frontend/` directory to Vercel or Netlify
**Backend:** Deploy `backend/` directory to Railway, Render, or similar
**Database:** PostgreSQL connection string (Neon already configured)

## License

MIT
