#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="inventory/output"
mkdir -p "$OUT_DIR"

TS="$(date +%Y%m%d-%H%M%S)"

az graph query -q "Resources | project resourceGroup, name, type, location, id, tags | order by resourceGroup asc, name asc" -o json > "$OUT_DIR/all-resources-$TS.json"

az graph query -q "Resources | where location =~ 'japaneast' | project resourceGroup, name, type, location, id, tags | order by resourceGroup asc, name asc" -o json > "$OUT_DIR/dr-jpe-resources-$TS.json"

echo "created: $OUT_DIR/all-resources-$TS.json"
echo "created: $OUT_DIR/dr-jpe-resources-$TS.json"
