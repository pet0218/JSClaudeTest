#!/bin/bash
# 1. Nahraď riadok nižšie svojím skutočným API kľúčom z console.anthropic.com
# 2. Ulož súbor
# 3. V chate spusti: ! bash analysis/run_analysis.sh

export ANTHROPIC_API_KEY="SEM_VLOZ_SVOJ_KLUC"
export ANTHROPIC_API_KEY="$(printf '%s' "$ANTHROPIC_API_KEY" | tr -d '\n\r ')"

cd "$(dirname "$0")"
source .venv/bin/activate
export PGHOST=localhost
export PGPORT=5433
export PGUSER=expense_tracker
export PGPASSWORD=expense_tracker
export PGDATABASE=expense_tracker
python suggest_investments_llm.py
