# AI Quote Tracker

Track and analyze quotes from US politicians and their staff about artificial intelligence. Paste a news article URL, and the app uses Claude to extract direct quotes, which you can review, edit, and save into a searchable database.

## Prerequisites

- Python 3.9+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

### Backend

```bash
cd backend

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run database migrations
python -m alembic upgrade head

# Start the server (port 8000)
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (port 5173, proxies /api to backend)
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Architecture

| Component | Tech |
|-----------|------|
| Backend | FastAPI, SQLAlchemy, SQLite, Alembic |
| LLM | Anthropic Claude claude-sonnet-4-20250514 |
| Article parsing | newspaper4k |
| Frontend | React, TypeScript, Vite, Tailwind CSS v4 |
| Data fetching | TanStack Query |
| Charts | Recharts |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/articles/extract` | Fetch article and extract AI quotes |
| POST | `/api/articles/save` | Save reviewed quotes to database |
| GET | `/api/people` | List all people (with `?search=`) |
| GET | `/api/people/:id` | Person detail with all quotes |
| PUT | `/api/people/:id` | Update person fields |
| GET | `/api/quotes` | List quotes with filters and pagination |
| GET | `/api/quotes/:id` | Single quote detail |
| PUT | `/api/quotes/:id` | Update quote |
| DELETE | `/api/quotes/:id` | Delete quote |
| GET | `/api/stats` | Dashboard statistics |
