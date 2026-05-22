#!/bin/bash
# Clean up all user JupyterLab instances

set -e

# Configuration
NAMESPACE="workshop"
NUM_USERS=${1:-50}

echo "========================================="
echo "Boston Tech Week 2026 - User Cleanup"
echo "========================================="
echo ""
echo "⚠️  WARNING: This will delete all JupyterLab instances!"
echo "   Namespace: $NAMESPACE"
echo "   Users: user1 - user$NUM_USERS"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Cleaning up..."
echo ""

for i in $(seq 1 $NUM_USERS); do
    USER_ID="user${i}"

    echo "Deleting $USER_ID..."

    # Delete all resources for this user
    oc delete deployment jupyter-${USER_ID} -n $NAMESPACE --ignore-not-found=true
    oc delete service jupyter-${USER_ID} -n $NAMESPACE --ignore-not-found=true
    oc delete route jupyter-${USER_ID} -n $NAMESPACE --ignore-not-found=true
    oc delete configmap workshop-notebook-${USER_ID} -n $NAMESPACE --ignore-not-found=true

    echo "  ✓ $USER_ID deleted"
done

echo ""
echo "========================================="
echo "Cleanup Complete!"
echo "========================================="
echo ""
echo "Verify cleanup:"
echo "  oc get all -n $NAMESPACE -l app=jupyter"
echo ""
