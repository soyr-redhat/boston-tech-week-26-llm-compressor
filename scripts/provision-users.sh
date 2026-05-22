#!/bin/bash
# Provision JupyterLab instances for workshop users

set -e

# Configuration
NAMESPACE="workshop"
NUM_USERS=${1:-50}
TEMPLATE="openshift/jupyter-user-template.yaml"
SECRET_KEY=${SECRET_KEY:-"boston-tech-week-2026-secret"}

# Function to generate deterministic suffix from user number
generate_suffix() {
    local user_num=$1
    echo -n "${SECRET_KEY}-user${user_num}" | sha256sum | cut -c1-10
}

echo "========================================="
echo "Boston Tech Week 2026 - User Provisioning"
echo "========================================="
echo ""
echo "Provisioning $NUM_USERS JupyterLab instances..."
echo ""

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "Template not found: $TEMPLATE"
    exit 1
fi

# Check if logged into OpenShift
if ! oc whoami &>/dev/null; then
    echo "Not logged into OpenShift. Please run 'oc login' first."
    exit 1
fi

# Create namespace if it doesn't exist
oc get namespace $NAMESPACE &>/dev/null || oc create namespace $NAMESPACE

# Process template for each user
for i in $(seq 1 $NUM_USERS); do
    USER_ID="user${i}"

    # Generate deterministic suffix (consistent with assignment app)
    SUFFIX=$(generate_suffix $i)

    echo "Provisioning $USER_ID-$SUFFIX..."

    oc process -f $TEMPLATE \
        -p USER_ID=$USER_ID \
        -p SUFFIX=$SUFFIX \
        --namespace=$NAMESPACE \
        | oc apply -n $NAMESPACE -f -

    echo "  $USER_ID-$SUFFIX deployed"
done

echo ""
echo "========================================="
echo "Provisioning Complete!"
echo "========================================="
echo ""
echo "Users should access via the assignment app:"
echo "  https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com"
echo ""
echo "Verify deployments:"
echo "  oc get pods -n $NAMESPACE -l app=jupyter"
echo ""
echo "Check routes:"
echo "  oc get routes -n $NAMESPACE -l app=jupyter"
echo ""
