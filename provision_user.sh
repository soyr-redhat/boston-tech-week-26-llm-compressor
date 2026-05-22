#!/bin/bash
# Provision a single user with their own vLLM instances and comparison UI

set -e

USER_NAME="${1}"
if [ -z "$USER_NAME" ]; then
    echo "Usage: ./provision_user.sh <username>"
    echo "Example: ./provision_user.sh user1"
    exit 1
fi

USER_NAMESPACE="workshop-${USER_NAME}"

echo "============================================"
echo "Provisioning: $USER_NAME"
echo "Namespace: $USER_NAMESPACE"
echo "============================================"

# Create namespace and ConfigMap
echo "[1/3] Creating namespace and ConfigMap..."
cat openshift/user-deployment.yaml | \
  sed "s/USER_NAMESPACE/${USER_NAMESPACE}/g" | \
  sed "s/USER_NAME/${USER_NAME}/g" | \
  oc apply -f -

# Create ConfigMap for UI code
oc create configmap comparison-ui-code \
  --from-file=comparison_ui.py \
  -n "${USER_NAMESPACE}" \
  --dry-run=client -o yaml | oc apply -f -

echo ""
echo "============================================"
echo "✅ User Provisioned: $USER_NAME"
echo "============================================"
echo ""
echo "URL: https://${USER_NAME}-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com"
echo ""
echo "Monitor:"
echo "  oc get pods -n ${USER_NAMESPACE} -w"
echo ""
