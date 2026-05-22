---
layout: default
title: Cluster Status
---

# OpenShift Cluster Status - Boston Tech Week 2026

**Last Updated:** 2026-05-22  
**Cluster:** https://console-openshift-console.apps.ocp.ntdrq.sandbox503.opentlc.com  
**Namespace:** workshop-user1

---

## Running Services

### vLLM Original Model (FP16)
- **Pod:** `vllm-original-6784c755c5-dxhhc`
- **Status:** ✅ Running with tensor parallelism
- **Model:** Qwen/Qwen2.5-7B-Instruct
- **Precision:** FP16
- **Context Length:** 8192 tokens
- **GPUs:** 2× NVIDIA L4 (46GB total VRAM)
- **Tensor Parallel Size:** 2
- **Internal Service:** vllm-original:8080
- **Public Endpoint:** https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com
- **Health Check:** ✅ Responding

### vLLM Quantized Model (INT4)
- **Pod:** `vllm-quantized-bf87465f9-6krlj`
- **Status:** ✅ Running with tensor parallelism
- **Model:** RedHatAI/Qwen3.5-9B-quantized.w4a16
- **Precision:** INT4 (w4a16 = 4-bit weights, 16-bit activations)
- **Context Length:** 8192 tokens
- **GPUs:** 2× NVIDIA L4 (46GB total VRAM)
- **Tensor Parallel Size:** 2
- **Internal Service:** vllm-quantized:8081
- **Public Endpoint:** https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com
- **Health Check:** ✅ Responding

### Comparison UI (Gradio)
- **Pod:** `comparison-ui-5977cc6cf9-rdfdk`
- **Status:** ✅ Running (59 minutes uptime)
- **Framework:** Gradio 5.x + Python 3.12
- **Theme:** Everforest (custom CSS)
- **Features:** Concurrent streaming, live metrics, side-by-side comparison
- **Internal Service:** comparison-ui:7860
- **Public URL:** https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
- **Health Check:** ✅ Accessible

---

## Resource Usage

### GPU Allocation
- **Total GPUs:** 4× NVIDIA L4 (23GB VRAM each)
- **Used:** 4 GPUs (100% utilized)
  - 2× vllm-original (tensor parallel)
  - 2× vllm-quantized (tensor parallel)
- **Available:** 0 GPUs
- **Benefits of 2 GPUs:** Higher throughput for 50 concurrent users

### Compute Resources
- **vllm-original:**
  - Requests: 4 CPU, 8GB RAM, 2 GPUs
  - Limits: 8 CPU, 16GB RAM, 2 GPUs
  - Tensor Parallel: 2
- **vllm-quantized:**
  - Requests: 4 CPU, 8GB RAM, 2 GPUs
  - Limits: 8 CPU, 16GB RAM, 2 GPUs
  - Tensor Parallel: 2
- **comparison-ui:**
  - Requests: 500m CPU, 1GB RAM
  - Limits: 1 CPU, 2GB RAM

### Storage
- **Model Weights:** ~40GB total
  - Qwen2.5-7B-Instruct: ~14GB (FP16)
  - Qwen3.5-9B-quantized: ~5GB (INT4)
  - HuggingFace cache: ~21GB

---

## Network Routes

| Service | Internal | External |
|---------|----------|----------|
| Original Model | vllm-original:8080 | https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com |
| Quantized Model | vllm-quantized:8081 | https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com |
| Comparison UI | comparison-ui:7860 | https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com |

All routes use TLS edge termination with automatic redirect from HTTP.

---

## API Endpoints

### Original Model (FP16)
```bash
# List models
curl https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models

# Generate completion
curl -X POST https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "prompt": "Hello",
    "max_tokens": 50
  }'

# Health check
curl https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/health
```

### Quantized Model (INT4)
```bash
# List models
curl https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models

# Generate completion
curl -X POST https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "RedHatAI/Qwen3.5-9B-quantized.w4a16",
    "prompt": "Hello",
    "max_tokens": 50
  }'

# Health check
curl https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/health
```

---

## Management Commands

### Check Pod Status
```bash
oc get pods -n workshop-user1
oc describe pod vllm-original-55ffd6c7d5-lxknk -n workshop-user1
```

### View Logs
```bash
# Follow logs (real-time)
oc logs -f deployment/vllm-original -n workshop-user1
oc logs -f deployment/vllm-quantized -n workshop-user1
oc logs -f deployment/comparison-ui -n workshop-user1

# Last 50 lines
oc logs deployment/vllm-original -n workshop-user1 --tail=50
```

### Restart Services
```bash
# Restart a deployment
oc rollout restart deployment/vllm-original -n workshop-user1
oc rollout restart deployment/vllm-quantized -n workshop-user1
oc rollout restart deployment/comparison-ui -n workshop-user1

# Watch restart progress
oc rollout status deployment/vllm-original -n workshop-user1
```

### Scale Resources
```bash
# Scale replicas
oc scale deployment/vllm-original --replicas=0 -n workshop-user1  # Stop
oc scale deployment/vllm-original --replicas=1 -n workshop-user1  # Start

# Update resource limits
oc set resources deployment/vllm-original \
  --limits=cpu=8,memory=16Gi \
  -n workshop-user1
```

### Access Pod Shell
```bash
oc exec -it deployment/vllm-original -n workshop-user1 -- /bin/bash
```

---

## Monitoring

### CPU/Memory Usage
```bash
oc adm top pods -n workshop-user1
```

### Events
```bash
oc get events -n workshop-user1 --sort-by='.lastTimestamp'
```

### Routes Status
```bash
oc get routes -n workshop-user1
```

---

## Known Issues

### None Currently

All services running stable with no errors.

### Previous Issues (Resolved)
- ✅ Permission denied on `/.local` - Fixed with `HOME=/tmp`
- ✅ Model name detection - Fixed with `/v1/models` endpoint query
- ✅ OOM on context length - Fixed with `--max-model-len 8192`
- ✅ FP8 model crashes - Switched to standard FP16 original model
- ✅ UI layout issues - Redesigned with Everforest theme

---

## Backup & Recovery

### If Pod Crashes
```bash
# Check logs for root cause
oc logs deployment/vllm-original -n workshop-user1 --previous

# Restart deployment
oc rollout restart deployment/vllm-original -n workshop-user1

# If persistent issues, delete and recreate
oc delete deployment vllm-original -n workshop-user1
oc apply -f openshift/user-deployment.yaml
```

### If Out of Memory
```bash
# Reduce context length in deployment
# Edit command args to use --max-model-len 4096 instead of 8192
oc edit deployment vllm-original -n workshop-user1
```

### If Route Unreachable
```bash
# Check route exists
oc get route vllm-original-api -n workshop-user1

# Recreate route if missing
oc expose service vllm-original --name=vllm-original-api -n workshop-user1
```

---

## Workshop Capacity

### Current Configuration
- **Instructor Demo:** 1 user (user1 namespace)
- **Participant Access:** 50 users via guidellm to shared APIs
- **GPU Utilization:** 2/4 GPUs (50%)
- **Expected Load:** Moderate (guidellm from 50 laptops)

### Load Handling
- Both vLLM instances can handle concurrent requests
- Automatic queueing when overloaded
- Expect 50-100 requests/minute during hands-on session
- P95 latency may increase under heavy load (expected behavior)

---

## Security

- ✅ TLS enabled on all routes (edge termination)
- ✅ Namespace isolation (workshop-user1)
- ✅ Resource limits prevent runaway consumption
- ✅ No authentication required (public workshop)
- ✅ Read-only access for participants (APIs only)

---

## Contact & Support

**OpenShift Console:** https://console-openshift-console.apps.ocp.ntdrq.sandbox503.opentlc.com  
**Logged in as:** cluster-admin  
**Namespace:** workshop-user1  
**Region:** AWS us-east-1 (assumed)

**For issues during workshop:**
1. Check this document first
2. Review pod logs: `oc logs deployment/<name> -n workshop-user1`
3. Restart if needed: `oc rollout restart deployment/<name> -n workshop-user1`

---

**Status:** ✅ ALL SYSTEMS OPERATIONAL - READY FOR WORKSHOP
