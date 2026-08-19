#!/bin/bash
set -e

DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-ksi_opinion_base}"
DB_PASSWORD="${DB_PASSWORD:-ksi_opinion_base}"
DB_NAME="${DB_NAME:-ksi_opinion_base}"
export PGPASSWORD="$DB_PASSWORD"

echo "Waiting for postgres at $DB_HOST:$DB_PORT..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" >/dev/null 2>&1; do
  sleep 1
done

echo "Checking if database schema is already initialized..."
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tc "SELECT 1 FROM department LIMIT 1;" 2>/dev/null | grep -q 1; then
  echo "Database already initialized."
else
  echo "Initializing database schema..."
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f /app/database/create.sql
  echo "Loading seed data..."
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f /app/database/input.sql
fi

echo "Resetting id sequences (idempotent)..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -tc "
SELECT setval(pg_get_serial_sequence('department', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM department;
SELECT setval(pg_get_serial_sequence('semester', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM semester;
SELECT setval(pg_get_serial_sequence('lecturers_roles', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM lecturers_roles;
SELECT setval(pg_get_serial_sequence('lecturers', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM lecturers;
SELECT setval(pg_get_serial_sequence('subjects', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM subjects;
SELECT setval(pg_get_serial_sequence('subject_groups', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM subject_groups;
SELECT setval(pg_get_serial_sequence('time', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM time;
SELECT setval(pg_get_serial_sequence('opinions', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM opinions;
SELECT setval(pg_get_serial_sequence('active_subjects', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM active_subjects;
SELECT setval(pg_get_serial_sequence('subject_subject_group_relation', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM subject_subject_group_relation;
SELECT setval(pg_get_serial_sequence('subjects_opinion_relation', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM subjects_opinion_relation;
SELECT setval(pg_get_serial_sequence('lecturers_opinion_relation', 'id'), COALESCE(max(id), 1), max(id) IS NOT NULL) FROM lecturers_opinion_relation;
"

echo "Loading USOS data from JSON files..."
python /app/database/load_usos_data.py

echo "Loader finished."
