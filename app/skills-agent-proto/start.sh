#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEB_DIR="$ROOT_DIR/web"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
API_BASE_URL="${VITE_API_BASE_URL:-http://127.0.0.1:${BACKEND_PORT}}"

BACKEND_PID=""
FRONTEND_PID=""

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[start] Missing required command: $cmd"
    exit 1
  fi
}

cleanup() {
  trap - EXIT INT TERM

  if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi

  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi

  wait "$FRONTEND_PID" "$BACKEND_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

require_cmd uv
require_cmd npm

if [[ ! -d "$WEB_DIR" ]]; then
  echo "[start] Frontend directory not found: $WEB_DIR"
  exit 1
fi

echo "[start] Installing backend dependencies with uv sync..."
cd "$ROOT_DIR"
uv sync

echo "[start] Installing frontend dependencies with npm install..."
cd "$WEB_DIR"
npm install

echo "[start] Starting backend on :$BACKEND_PORT ..."
cd "$ROOT_DIR"
SKILLS_WEB_HOST="0.0.0.0" \
SKILLS_WEB_PORT="$BACKEND_PORT" \
SKILLS_WEB_RELOAD="true" \
uv run langchain-skills-web &
BACKEND_PID=$!

echo "[start] Starting frontend on :$FRONTEND_PORT ..."
cd "$WEB_DIR"
VITE_API_BASE_URL="$API_BASE_URL" \
npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT" &
FRONTEND_PID=$!

echo "[start] Backend:  http://127.0.0.1:$BACKEND_PORT"
echo "[start] Frontend: http://127.0.0.1:$FRONTEND_PORT"
echo "[start] Press Ctrl+C to stop both services."

SERVICE_EXIT_CODE=0
while true; do
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    wait "$BACKEND_PID" || SERVICE_EXIT_CODE=$?
    break
  fi

  if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    wait "$FRONTEND_PID" || SERVICE_EXIT_CODE=$?
    break
  fi

  sleep 1
done

echo "[start] One service exited, shutting down..."
exit "$SERVICE_EXIT_CODE"
