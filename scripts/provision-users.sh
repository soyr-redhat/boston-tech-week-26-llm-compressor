#!/bin/bash
# Provision JupyterLab instances for workshop users

set -e

# Configuration
NAMESPACE="workshop"
NUM_USERS=${1:-50}
TEMPLATE="openshift/jupyter-user-template.yaml"

echo "========================================="
echo "Boston Tech Week 2026 - User Provisioning"
echo "========================================="
echo ""
echo "Provisioning $NUM_USERS JupyterLab instances..."
echo ""

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "❌ Template not found: $TEMPLATE"
    exit 1
fi

# Check if logged into OpenShift
if ! oc whoami &>/dev/null; then
    echo "❌ Not logged into OpenShift. Please run 'oc login' first."
    exit 1
fi

# Create namespace if it doesn't exist
oc get namespace $NAMESPACE &>/dev/null || oc create namespace $NAMESPACE

# Process template for each user
for i in $(seq 1 $NUM_USERS); do
    USER_ID="user${i}"

    echo "Provisioning $USER_ID..."

    oc process -f $TEMPLATE \
        -p USER_ID=$USER_ID \
        --namespace=$NAMESPACE \
        | oc apply -n $NAMESPACE -f -

    echo "  ✓ $USER_ID deployed"
done

echo ""
echo "========================================="
echo "Provisioning Complete!"
echo "========================================="
echo ""
echo "User URLs:"
echo ""

for i in $(seq 1 $NUM_USERS); do
    USER_ID="user${i}"
    URL="https://jupyter-${USER_ID}.apps.ocp.ntdrq.sandbox503.opentlc.com"
    echo "  $USER_ID: $URL"
done

echo ""
echo "Verify deployments:"
echo "  oc get pods -n $NAMESPACE -l app=jupyter"
echo ""
echo "Check routes:"
echo "  oc get routes -n $NAMESPACE -l app=jupyter"
echo ""
