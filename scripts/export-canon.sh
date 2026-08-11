#!/bin/bash
# export-canon.sh — canon snapshot export (CLAUDE.md "Canon snapshot export").
#
# Reader law: every canon read in this repo filters status='active'; retired
# facts must never reach a pack or a hint. Origin: dashboard-retire-record.md §3.
#
# Rides the existing ssh → docker exec → psql loopback path. Reads container/
# user/db NAMES from the work-automation .env at run time; values never printed.
#
# Expected output (counts move as canon moves; active == total → STOP):
#   exported NNN active canon rows → pack/canon.json
#   total canon rows: MMM
#   filter check: active (NNN) < total (MMM) — OK
set -euo pipefail

cd "$(dirname "$0")/.."

ENV_FILE="$HOME/dev/work-automation/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "STOP: $ENV_FILE not found (needed for PG_CONTAINER/PG_USER/PG_DB names)" >&2
  exit 1
fi
PG_CONTAINER=$(grep '^PG_CONTAINER=' "$ENV_FILE" | cut -d= -f2-)
PG_USER=$(grep '^PG_USER=' "$ENV_FILE" | cut -d= -f2-)
PG_DB=$(grep '^PG_DB=' "$ENV_FILE" | cut -d= -f2-)
if [ -z "$PG_CONTAINER" ] || [ -z "$PG_USER" ] || [ -z "$PG_DB" ]; then
  echo "STOP: PG_CONTAINER/PG_USER/PG_DB missing from $ENV_FILE" >&2
  exit 1
fi

QUERY="SELECT json_agg(t) FROM (SELECT id, fact_text, structured_value, tier, volatility_class, shareability, verified_at FROM pkms_canon WHERE status='active') t"

mkdir -p pack
ssh eq14 "docker exec $PG_CONTAINER psql -U $PG_USER -d $PG_DB -Atc \"$QUERY\"" > pack/canon.json

ACTIVE=$(python3 -c "import json; print(len(json.load(open('pack/canon.json'))))") || {
  echo "STOP: pack/canon.json is not a JSON array — export failed" >&2
  exit 1
}
echo "exported $ACTIVE active canon rows → pack/canon.json"

TOTAL=$(ssh eq14 "docker exec $PG_CONTAINER psql -U $PG_USER -d $PG_DB -Atc \"SELECT count(*) FROM pkms_canon\"")
echo "total canon rows: $TOTAL"

if [ "$ACTIVE" -eq "$TOTAL" ]; then
  echo "STOP: active count equals total ($TOTAL) — the status='active' filter is missing or nothing is retired. Failure signature per CLAUDE.md; do NOT build a pack from this export." >&2
  exit 1
fi
echo "filter check: active ($ACTIVE) < total ($TOTAL) — OK"
