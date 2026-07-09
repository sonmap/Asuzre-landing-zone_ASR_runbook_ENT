#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-}"
ACTION="${2:-plan}"

if [ -z "$ROOT" ]; then
  echo "Usage: tools/tf_root.sh <terraform-root> <init|validate|plan|apply|destroy>"
  exit 1
fi

if [ ! -d "$ROOT" ]; then
  echo "Terraform root not found: $ROOT"
  exit 1
fi

if [ ! -f "backend.hcl" ]; then
  echo "backend.hcl not found. Copy backend.hcl.example to backend.hcl first."
  exit 1
fi

STATE_KEY="${ROOT#live/}.tfstate"

echo "## Root: $ROOT"
echo "## Action: $ACTION"
echo "## State key: $STATE_KEY"

terraform -chdir="$ROOT" init -backend-config=../../../backend.hcl -backend-config="key=$STATE_KEY"

case "$ACTION" in
  init)
    ;;
  validate)
    terraform -chdir="$ROOT" validate
    ;;
  plan)
    terraform -chdir="$ROOT" plan
    ;;
  apply)
    terraform -chdir="$ROOT" apply
    ;;
  destroy)
    terraform -chdir="$ROOT" destroy
    ;;
  *)
    echo "Unsupported action: $ACTION"
    exit 1
    ;;
esac
