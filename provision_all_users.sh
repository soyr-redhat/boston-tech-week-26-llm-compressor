#!/bin/bash
# Provision all workshop users

set -e

NUM_USERS="${1:-20}"

echo "============================================"
echo "Provisioning $NUM_USERS Users"
echo "============================================"
echo ""
echo "⚠️  WARNING: Each user needs 2 GPUs"
echo "   With 4 GPUs total, max 2 users can run simultaneously"
echo "   Recommend provisioning users but having them start/stop as needed"
echo ""

read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

for i in $(seq 1 $NUM_USERS); do
    USER_NAME="user${i}"
    echo ""
    echo "[$i/$NUM_USERS] Provisioning $USER_NAME..."
    ./provision_user.sh "$USER_NAME"
    sleep 2
done

echo ""
echo "============================================"
echo "✅ All Users Provisioned"
echo "============================================"
echo ""
echo "Generate URL list:"
echo "  ./get_user_urls.sh"
echo ""
echo "⚠️  Users should start their vLLM instances when ready:"
echo "  oc scale deployment/vllm-original --replicas=1 -n workshop-user1"
echo "  oc scale deployment/vllm-quantized --replicas=1 -n workshop-user1"
echo ""
