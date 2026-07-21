#!/bin/sh
# Force-kills the entire docker-compose stack (db, api, web).
# Containers are stopped but not removed - use start-stack.sh to bring them back.

set -e
cd "$(dirname "$0")/.."

docker compose kill
