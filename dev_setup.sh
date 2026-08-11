#!/usr/bin/env bash
#
# One-shot dev playground setup:
#   Postgres (docker) -> schema + seed -> fix sequences -> load USOS JSON -> API -> Swagger UI
#
# Usage:
#   ./dev_setup.sh            full setup + start API + open Swagger UI
#   ./dev_setup.sh --setup-only   setup data, print how to start API, do NOT start it
#   ./dev_setup.sh --no-reset     keep existing DB data, just (re)start API
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
DATABASE_DIR="$ROOT_DIR/database"

CONTAINER="ksi_opinion_base"
DB_PORT="5434"
API_PORT="8000"
DB_USER="ksi_opinion_base"
DB_PASS="ksi_opinion_base"
DB_NAME="ksi_opinion_base"
PG_IMAGE="postgres:18"

SETUP_ONLY=0
RESET=1

for arg in "$@"; do
    case "$arg" in
        --setup-only) SETUP_ONLY=1 ;;
        --no-reset) RESET=0 ;;
        *) echo "unknown option: $arg" >&2; exit 1 ;;
    esac
done

# ---------------------------------------------------------------- docker check
command -v docker >/dev/null 2>&1 || {
    echo "ERROR: docker is not installed / not on PATH" >&2
    exit 1
}

# ------------------------------------------------------- ensure postgres runs
if docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "[ok] postgres container '$CONTAINER' already running"
elif docker ps --format '{{.Names}} {{.Ports}}' | grep -q "0.0.0.0:$DB_PORT->"; then
    echo "ERROR: port $DB_PORT is already used by another container." >&2
    echo "       Stop it first, e.g.:  docker rm -f <container-name>" >&2
    docker ps --format '{{.Names}} {{.Ports}}' | grep "0.0.0.0:$DB_PORT->" >&2
    exit 1
else
    echo "[*] starting postgres container '$CONTAINER' ($PG_IMAGE)..."
    docker run -d --name "$CONTAINER" \
        -e POSTGRES_USER="$DB_USER" \
        -e POSTGRES_PASSWORD="$DB_PASS" \
        -e POSTGRES_DB="$DB_NAME" \
        -p "$DB_PORT:5432" \
        "$PG_IMAGE"
fi

echo "[*] waiting for postgres to accept connections..."
until docker exec "$CONTAINER" pg_isready -U "$DB_USER" -d "$DB_NAME" >/dev/null 2>&1; do
    sleep 1
done

psql() {
    docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 "$@"
}

# --------------------------------------------------------------- reset database
if [ "$RESET" -eq 1 ]; then
    echo "[*] resetting database (clear -> create -> seed)..."
    psql < "$DATABASE_DIR/clear.sql" >/dev/null
    psql < "$DATABASE_DIR/create.sql" >/dev/null
    psql < "$DATABASE_DIR/input.sql" >/dev/null

    echo "[*] fixing serial sequences (seed used explicit ids via COPY)..."
    psql <<'SQL'
SELECT setval(pg_get_serial_sequence('lecturers','id'), (SELECT COALESCE(max(id),1) FROM lecturers));
SELECT setval(pg_get_serial_sequence('subjects','id'), (SELECT COALESCE(max(id),1) FROM subjects));
SELECT setval(pg_get_serial_sequence('active_subjects','id'), (SELECT COALESCE(max(id),1) FROM active_subjects));
SQL
    echo "[*] loading USOS JSON data..."
    if command -v uv >/dev/null 2>&1; then
        ( cd "$BACKEND_DIR" && uv run python app/services/load_usos_data.py )
    else
        ( cd "$BACKEND_DIR" && python app/services/load_usos_data.py )
    fi
else
    echo "[*] --no-reset: keeping existing database data"
fi

# ---------------------------------------------------------------- sanity counts
echo "[*] row counts:"
psql -c "SELECT (SELECT count(*) FROM lecturers) AS lecturers,
                (SELECT count(*) FROM subjects) AS subjects,
                (SELECT count(*) FROM active_subjects) AS active_subjects;"

if [ "$SETUP_ONLY" -eq 1 ]; then
    echo
    echo "Setup complete. Start the API yourself with:"
    echo "  cd $BACKEND_DIR && uv run uvicorn main:app --reload --port $API_PORT"
    echo "then open http://localhost:$API_PORT/docs"
    exit 0
fi

# ---------------------------------------------------------------------- run API
command -v uv >/dev/null 2>&1 && RUNNER=(uv run) || RUNNER=()
command -v xdg-open >/dev/null 2>&1 && OPEN=1 || OPEN=0

echo
echo "[*] starting API on http://localhost:$API_PORT/docs ..."
if [ "$OPEN" -eq 1 ]; then
    ( sleep 2; xdg-open "http://localhost:$API_PORT/docs" >/dev/null 2>&1 ) &
fi
echo "    (Ctrl+C to stop the API; postgres container '$CONTAINER' keeps running)"
echo "    cleanup later with:  docker rm -f $CONTAINER"
echo

cd "$BACKEND_DIR"
if [ "${#RUNNER[@]}" -gt 0 ]; then
    exec "${RUNNER[@]}" uvicorn main:app --port "$API_PORT"
else
    exec uvicorn main:app --port "$API_PORT"
fi
