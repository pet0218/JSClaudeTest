#!/bin/sh
# Revives the docker-compose stack (db, api, web) if all containers are stopped/killed.
# If anything is already running, does nothing.

set -e
cd "$(dirname "$0")/.."

running=$(docker compose ps -q)

if [ -z "$running" ]; then
  echo "Žiadny kontajner nebeží, štartujem stack..."
  docker compose up -d
else
  echo "Stack už beží, nič nerobím."
  docker compose ps
fi
