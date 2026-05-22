
# OpenShift Cluster Status - Boston Tech Week 2026

**Last Updated:** 2026-05-22  
**Cluster:** https://console-openshift-console.apps.ocp.ntdrq.sandbox503.opentlc.com  
**Namespace:** workshop-user1


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


## Security

-  TLS enabled on all routes (edge termination)
-  Namespace isolation (workshop-user1)
-  Resource limits prevent runaway consumption
-  No authentication required (public workshop)
-  Read-only access for participants (APIs only)


**Status:**  ALL SYSTEMS OPERATIONAL - READY FOR WORKSHOP
