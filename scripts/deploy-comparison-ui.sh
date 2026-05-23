#!/bin/bash

# Deploy comparison UI to OpenShift
# Creates/updates ConfigMap with comparison_ui.py and deploys the service

set -e

NAMESPACE="${NAMESPACE:-workshop}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Deploying comparison UI to namespace: $NAMESPACE"
echo ""

# Create/update ConfigMap from comparison_ui.py
echo "Creating ConfigMap from apps/comparison_ui.py..."
oc create configmap comparison-ui-code \
    --from-file=comparison_ui.py="$PROJECT_ROOT/apps/comparison_ui.py" \
    --namespace="$NAMESPACE" \
    --dry-run=client -o yaml | oc apply -f -

echo "✓ ConfigMap created/updated"
echo ""

# Check if deployment exists, restart it to pick up new code
if oc get deployment comparison-ui -n "$NAMESPACE" &>/dev/null; then
    echo "Restarting comparison-ui deployment..."
    oc rollout restart deployment/comparison-ui -n "$NAMESPACE"
    echo "✓ Deployment restarted"
else
    echo "⚠ comparison-ui deployment not found. Deploy it first with:"
    echo "  oc apply -f openshift/workshop-deployment.yaml"
fi

echo ""
echo "Done! Comparison UI updated."
