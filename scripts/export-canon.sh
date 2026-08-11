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
#   db counts: active NNN / total MMM
#   filter check: active (NNN) < total (MMM), json length matches db active — OK
#   manifest: pack/manifest.json written
#
# Amendment A1 (2026-08-11): filter verification lives HERE, at export time,
# where DB truth is queryable. Writes pack/manifest.json {exported_at,
# active_count, total_count, sha256}; the loop loader refuses to start unless
# pack length == manifest.active_count and sha256 matches.
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

# A1: both counts in one DB session; JSON length must match db active count.
COUNTS=$(ssh eq14 "docker exec $PG_CONTAINER psql -U $PG_USER -d $PG_DB -Atc \"SELECT count(*) FILTER (WHERE status='active'), count(*) FROM pkms_canon\"")
DB_ACTIVE=$(echo "$COUNTS" | cut -d'|' -f1)
TOTAL=$(echo "$COUNTS" | cut -d'|' -f2)
echo "db counts: active $DB_ACTIVE / total $TOTAL"

if [ "$ACTIVE" -ne "$DB_ACTIVE" ]; then
  echo "STOP: json length ($ACTIVE) != db active count ($DB_ACTIVE) — export and count disagree; do NOT build a pack from this export." >&2
  exit 1
fi
if [ "$ACTIVE" -eq "$TOTAL" ]; then
  echo "STOP: active count equals total ($TOTAL) — the status='active' filter is missing or nothing is retired. Failure signature per CLAUDE.md; do NOT build a pack from this export." >&2
  exit 1
fi
echo "filter check: active ($ACTIVE) < total ($TOTAL), json length matches db active — OK"

python3 - "$ACTIVE" "$TOTAL" <<'EOF'
import hashlib, json, sys, datetime
active, total = int(sys.argv[1]), int(sys.argv[2])
sha = hashlib.sha256(open("pack/canon.json", "rb").read()).hexdigest()
json.dump({"exported_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "active_count": active, "total_count": total, "sha256": sha},
          open("pack/manifest.json", "w"), indent=1)
EOF
echo "manifest: pack/manifest.json written"
