#!/usr/bin/env bash
set -euo pipefail

EXCEL="${1:-azure_landingzone_terraform_module_design.xlsx}"
TENANT_ID="${TENANT_ID:-}"
SUBSCRIPTION_ID="${SUBSCRIPTION_ID:-}"
LOCATION="${LOCATION:-koreacentral}"
DR_LOCATION="${DR_LOCATION:-japaneast}"

if [ -z "$TENANT_ID" ]; then
  echo "ERROR: TENANT_ID environment variable is required."
  exit 1
fi

if [ -z "$SUBSCRIPTION_ID" ]; then
  echo "ERROR: SUBSCRIPTION_ID environment variable is required."
  exit 1
fi

if [ ! -f "$EXCEL" ]; then
  echo "ERROR: Excel file not found: $EXCEL"
  exit 1
fi

echo "## Generate primary center tfvars: 00/10/20/30/40"
python3 tools/excel_to_tfvars.py \
  --excel "$EXCEL" \
  --out live \
  --tenant-id "$TENANT_ID" \
  --subscription-id "$SUBSCRIPTION_ID" \
  --location "$LOCATION"

echo "## Generate DR / ASR / Operations tfvars: D00/D10/D20/D30/D40/50-asr/60-operations"
python3 tools/excel_to_tfvars_dr.py \
  --excel "$EXCEL" \
  --out live \
  --tenant-id "$TENANT_ID" \
  --subscription-id "$SUBSCRIPTION_ID" \
  --dr-location "$DR_LOCATION"

echo "## Completed. Generated terraform.tfvars files are under live/."
