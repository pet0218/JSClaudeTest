#!/bin/sh
# Connects to the running Postgres container and prints all reports.
# Usage: ./scripts/list-reports.sh [--json]

set -e

CONTAINER=expense-tracker-starter-db-1
DB_USER=expense_tracker
DB_NAME=expense_tracker

if [ "$1" = "--json" ]; then
  docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -t -c \
    "SELECT COALESCE(json_agg(row_to_json(r)), '[]') FROM (
       SELECT id, employee_name AS \"employeeName\", employee_id AS \"employeeId\", problem, created_at AS \"createdAt\"
       FROM reports ORDER BY created_at
     ) r;"
else
  docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c \
    "SELECT id, employee_name, employee_id, problem, created_at FROM reports ORDER BY created_at;"
fi
