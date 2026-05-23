# Infrastructure Status

**Cluster:** OpenShift 4.x  
**Namespace:** `workshop`

---

## Deployed Services

### vLLM Models

| Service | Model | GPUs | Endpoints |
|---------|-------|------|-----------|
| vllm-original | Qwen/Qwen2.5-7B-Instruct (FP16) | 2x L4 | <a href="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com" target="_blank">https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com</a> |
| vllm-quantized | RedHatAI/Qwen3.5-9B-quantized.w4a16 (INT4) | 2x L4 | <a href="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com" target="_blank">https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com</a> |

### Workshop Infrastructure

| Service | Purpose | URL |
|---------|---------|-----|
| Assignment App | Auto-assign users to workspaces | <a href="https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com" target="_blank">https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com</a> |
| Comparison UI | Instructor demo interface | <a href="https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com" target="_blank">https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com</a> |
| JupyterLab (50x) | Per-user notebook environments | https://jupyter-user{N}-{suffix}.apps... |

---

## Resource Usage

### GPU Allocation
- **Total:** 4x NVIDIA L4 (23GB VRAM each)
- **vllm-original:** 2 GPUs (tensor parallel)
- **vllm-quantized:** 2 GPUs (tensor parallel)
- **JupyterLab instances:** No GPU (CPU-only benchmarking)

### Compute Resources
```yaml
vllm-original:
  requests: 4 CPU, 8GB RAM, 2 GPUs
  limits: 8 CPU, 16GB RAM, 2 GPUs
  
vllm-quantized:
  requests: 4 CPU, 8GB RAM, 2 GPUs
  limits: 8 CPU, 16GB RAM, 2 GPUs

jupyter (per user):
  requests: 500m CPU, 2GB RAM
  limits: 1 CPU, 4GB RAM

comparison-ui:
  requests: 500m CPU, 1GB RAM
  limits: 1 CPU, 2GB RAM

assignment-app:
  requests: 100m CPU, 256MB RAM
  limits: 200m CPU, 512MB RAM
```

### Storage
- **Model Weights:** ~20GB cached in pods
- **JupyterLab home dirs:** emptyDir (ephemeral)
- **Assignment state:** /tmp in assignment app pod

---

## Health Checks

### Check Pod Status
```bash
oc get pods -n workshop
```

### Test vLLM Endpoints
```bash
# Original model
curl https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models

# Quantized model
curl https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models
```

### Check Assignment App
```bash
curl https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com/status
```

### View User Workspaces
```bash
oc get pods -n workshop -l app=jupyter
oc get routes -n workshop -l app=jupyter
```

---

## Common Operations

### Reset Assignment Counter
```bash
curl https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com/reset
```

### Restart a Service
```bash
# Restart vLLM pod
oc rollout restart deployment/vllm-original -n workshop

# Restart assignment app
oc delete pod -n workshop -l app=workshop-assignment
```

### View Logs
```bash
# vLLM logs
oc logs -f deployment/vllm-original -n workshop

# Assignment app logs
oc logs -f deployment/workshop-assignment -n workshop

# User JupyterLab logs
oc logs deployment/jupyter-user1-{suffix} -n workshop
```

### Clean Up All User Workspaces
```bash
./scripts/cleanup-users.sh
```

---

## Troubleshooting

### vLLM Pod Won't Start

**Check events:**
```bash
oc describe pod -n workshop -l app=vllm-original
```

**Common issues:**
- Out of GPU memory → Reduce `--max-model-len`
- Image pull error → Check registry access
- Model download timeout → Check internet connectivity

### User Can't Access JupyterLab

**Check pod status:**
```bash
oc get pods -n workshop -l user=user1
```

**Check route:**
```bash
oc get route -n workshop | grep user1
```

**Verify NetworkPolicy:**
```bash
oc get networkpolicy -n workshop
```

### Assignment App Not Responding

**Check logs:**
```bash
oc logs deployment/workshop-assignment -n workshop
```

**Common issues:**
- Flask crashed → Check for Python errors in logs
- ConfigMap out of sync → Redeploy with `./scripts/deploy-assignment.sh`
- /tmp/assignments.json corrupted → Delete pod to reset state

---

## Security

- **TLS:** All routes use edge termination
- **Authentication:** None (60-min workshop, acceptable trade-off)
- **Isolation:** NetworkPolicy prevents pod-to-pod access between users
- **RBAC:** JupyterLab pods use default ServiceAccount (no cluster permissions)
- **URL Obfuscation:** Hash-based suffixes prevent user enumeration
