#!/bin/bash
# Provision JupyterLab instances for workshop users

set -e

# Configuration
NAMESPACE="workshop"
NUM_USERS=${1:-50}
TEMPLATE="openshift/jupyter-user-template.yaml"
TOKENS_FILE="user-tokens.json"

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

# Initialize tokens file
echo "{" > $TOKENS_FILE
echo "  \"tokens\": {" >> $TOKENS_FILE

# Process template for each user
for i in $(seq 1 $NUM_USERS); do
    USER_ID="user${i}"

    # Generate random token (32 bytes = 43 chars base64)
    TOKEN=$(openssl rand -base64 32 | tr -d '/+=' | cut -c1-43)

    echo "Provisioning $USER_ID..."

    oc process -f $TEMPLATE \
        -p USER_ID=$USER_ID \
        -p TOKEN=$TOKEN \
        --namespace=$NAMESPACE \
        | oc apply -n $NAMESPACE -f -

    # Store token in file
    if [ $i -lt $NUM_USERS ]; then
        echo "    \"$i\": \"$TOKEN\"," >> $TOKENS_FILE
    else
        echo "    \"$i\": \"$TOKEN\"" >> $TOKENS_FILE
    fi

    echo "  $USER_ID deployed"
done

# Close JSON file
echo "  }" >> $TOKENS_FILE
echo "}" >> $TOKENS_FILE

echo ""
echo "========================================="
echo "Provisioning Complete!"
echo "========================================="
echo ""
echo "Tokens saved to: $TOKENS_FILE"
echo ""
echo "IMPORTANT: Each user has a unique authentication token."
echo "Users should access via the assignment app:"
echo "  https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com"
echo ""
echo "Verify deployments:"
echo "  oc get pods -n $NAMESPACE -l app=jupyter"
echo ""
echo "Check routes:"
echo "  oc get routes -n $NAMESPACE -l app=jupyter"
echo ""
