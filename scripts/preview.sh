#!/usr/bin/env bash
#
# Build the frontend production bundle and serve it alongside the
# FastAPI backend — mirrors Vercel's architecture locally.
#
# Usage:  ./scripts/preview.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Building frontend production bundle..."
cd "$ROOT/frontend"
npm install --silent
npm run build

echo ""
echo "==> Starting backend (serves API on http://localhost:8000) ..."
echo "    Frontend preview: run 'cd frontend && npx vite preview' in another terminal"
echo ""
cd "$ROOT/backend"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
