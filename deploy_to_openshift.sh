#!/bin/bash
# One-command deployment to OpenShift

set -e

NAMESPACE="${1:-boston-tech-week-2026}"

echo "============================================"
echo "Deploying to OpenShift"
echo "Namespace: $NAMESPACE"
echo "============================================"
echo ""

# Check if logged in
if ! oc whoami &>/dev/null; then
    echo "❌ Not logged into OpenShift"
    echo "   Run: oc login <cluster-url>"
    exit 1
fi

echo "✅ Logged in as: $(oc whoami)"
echo ""

# Create namespace if it doesn't exist
if ! oc get namespace "$NAMESPACE" &>/dev/null; then
    echo "[1/4] Creating namespace..."
    oc create namespace "$NAMESPACE"
else
    echo "[1/4] Namespace already exists"
fi

# Create ConfigMap
echo "[2/4] Creating ConfigMap for UI code..."
oc create configmap comparison-ui-code \
    --from-file=comparison_ui.py \
    -n "$NAMESPACE" \
    --dry-run=client -o yaml | oc apply -f -

# Deploy vLLM models
echo "[3/4] Deploying vLLM models..."
oc apply -f openshift/deployment-vllm-original.yaml -n "$NAMESPACE"
oc apply -f openshift/deployment-vllm-quantized.yaml -n "$NAMESPACE"

# Deploy comparison UI
echo "[4/4] Deploying comparison UI..."
oc apply -f openshift/deployment-comparison-ui.yaml -n "$NAMESPACE"

echo ""
echo "============================================"
echo "Deployment Complete!"
echo "============================================"
echo ""

# Wait for pods
echo "Waiting for pods to start..."
sleep 5

oc get pods -n "$NAMESPACE"

echo ""
echo "Access URL:"
UI_HOST=$(oc get route comparison-ui -n "$NAMESPACE" -o jsonpath='{.spec.host}' 2>/dev/null || echo "pending...")
echo "  https://$UI_HOST"

echo ""
echo "Monitor deployment:"
echo "  oc get pods -n $NAMESPACE -w"
echo ""
echo "Check logs:"
echo "  oc logs -f deployment/vllm-original -n $NAMESPACE"
echo "  oc logs -f deployment/vllm-quantized -n $NAMESPACE"
echo "  oc logs -f deployment/comparison-ui -n $NAMESPACE"
echo ""
echo "Models will take 1-3 minutes to load. Watch logs for readiness."
echo ""
