# Per-User Deployment System

## Overview

Each workshop participant gets their own:
- ✅ Unique namespace (`workshop-user1`, `workshop-user2`, etc.)
- ✅ Own vLLM original model instance
- ✅ Own vLLM quantized model instance
- ✅ Own comparison UI
- ✅ **Unique URL:** `https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com`

## Quick Start

### Provision a Single User

```bash
./provision_user.sh user1
```

**Result:**
- Namespace: `workshop-user1`
- URL: `https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com`

### Provision Multiple Users

```bash
./provision_all_users.sh 20
```

Creates user1, user2, ..., user20 with unique URLs for each.

### Get All User URLs

```bash
./get_user_urls.sh
```

**Output:**
```
https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
https://user2-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
...
```

## Resource Requirements

### Per User:
- **2 GPUs** (1 for original, 1 for quantized model)
- **4-8 CPU cores**
- **8-16 GB RAM**

### Cluster Capacity:
- **4× L4 GPUs** available
- **Max concurrent users: 2** (2 users × 2 GPUs = 4 GPUs)

## Workshop Strategy

### Option 1: Staggered Access

**Pre-provision all 50 users**, but only 2 run at a time:

```bash
# Provision all users (creates namespaces, but scales deployments to 0)
./provision_all_users.sh 50

# Session 1 (11:00-11:30): Users 1-2
oc scale deployment/vllm-original --replicas=1 -n workshop-user1
oc scale deployment/vllm-quantized --replicas=1 -n workshop-user1
oc scale deployment/vllm-original --replicas=1 -n workshop-user2
oc scale deployment/vllm-quantized --replicas=1 -n workshop-user2

# Session 2 (11:30-12:00): Users 3-4
# Scale down 1-2, scale up 3-4...
```

### Option 2: Demo Mode

**1 instructor demo + shared read-only access:**

- Instructor uses `user1`
- All participants watch at: `https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com`
- Participants can experiment but instructor drives

### Option 3: Shared vLLM Backend

**50 users with unique UIs, but shared vLLM instances:**

```bash
# Deploy shared vLLM in main namespace
oc apply -f openshift/deployment-vllm-original.yaml -n workshop-shared
oc apply -f openshift/deployment-vllm-quantized.yaml -n workshop-shared

# Each user gets only their UI
# UIs point to workshop-shared:8080 and workshop-shared:8081
```

## User Experience

### User Receives:
- **Email:** "Your workshop URL: https://user5-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com"
- **Instructions:** "Open URL, try prompts, compare models"

### User Opens URL:
1. Sees Gradio comparison interface
2. Default endpoints pre-configured (8080 and 8081)
3. Can immediately start comparing models
4. Gets real-time metrics

## Management Commands

### Check All Users
```bash
oc get namespaces | grep workshop-
```

### Check Specific User
```bash
oc get pods -n workshop-user1
oc logs -f deployment/vllm-original -n workshop-user1
```

### Scale User Resources
```bash
# Start user's vLLM instances
oc scale deployment/vllm-original --replicas=1 -n workshop-user1
oc scale deployment/vllm-quantized --replicas=1 -n workshop-user1

# Stop user's vLLM instances (save GPUs)
oc scale deployment/vllm-original --replicas=0 -n workshop-user1
oc scale deployment/vllm-quantized --replicas=0 -n workshop-user1

# UI stays running (no GPU needed)
```

### Delete User
```bash
oc delete namespace workshop-user1
```

### Delete All Users
```bash
oc delete namespaces -l workshop=boston-tech-week-2026
```

## Automation Script

Create `start_user_session.sh`:

```bash
#!/bin/bash
# Start a user's session

USER=$1
NAMESPACE="workshop-${USER}"

echo "Starting session for $USER..."

# Scale up vLLM instances
oc scale deployment/vllm-original --replicas=1 -n $NAMESPACE
oc scale deployment/vllm-quantized --replicas=1 -n $NAMESPACE

# Wait for ready
echo "Waiting for models to load (60s)..."
sleep 60

# Get URL
URL=$(oc get route -n $NAMESPACE -o jsonpath='{.items[0].spec.host}')
echo ""
echo "Ready! URL: https://$URL"
```

## Cost Optimization

### Pre-provision All, Run Few

```bash
# Create all 50 user namespaces
./provision_all_users.sh 50

# All deployments start at 0 replicas (no cost)

# Only scale up during user's timeslot
./start_user_session.sh user1

# Scale down after
oc scale deployment/vllm-original --replicas=0 -n workshop-user1
oc scale deployment/vllm-quantized --replicas=0 -n workshop-user1
```

### Benefits:
- ✅ Each user gets unique URL
- ✅ Only 2 users active at a time (4 GPUs total)
- ✅ No resource waste
- ✅ Easy to manage

## URL Format

All URLs follow pattern:
```
https://{username}-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
```

Examples:
- user1: https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
- user2: https://user2-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
- alice: https://alice-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com

## Testing

### Test User1
```bash
# Provision
./provision_user.sh user1

# Wait for pods
oc get pods -n workshop-user1 -w

# Test vLLM
oc exec -n workshop-user1 deployment/vllm-original -- \
  curl -s http://localhost:8080/health

# Get URL
URL=$(oc get route comparison-ui -n workshop-user1 -o jsonpath='{.spec.host}')
echo "https://$URL"

# Open in browser and test!
```

## Recommended Workshop Flow

**Before Workshop:**
1. Provision all 50 users: `./provision_all_users.sh 50`
2. Generate URL list: `./get_user_urls.sh > user_urls.txt`
3. Email each user their unique URL

**During Workshop:**
- **Option A:** 25 parallel sessions of 2 users each (rotate every 2 min)
- **Option B:** Instructor demo with user1, others observe
- **Option C:** Use shared vLLM backend for all UIs

**After Workshop:**
```bash
# Cleanup everything
oc delete namespaces -l workshop=boston-tech-week-2026
```

## Current Status

✅ Per-user system created
✅ Tested with user1 and user2
✅ Unique URLs working
✅ vLLM instances deploying per user
✅ Ready to provision all 50 users

**Next:** Decide on workshop strategy (staggered, demo, or shared backend)
