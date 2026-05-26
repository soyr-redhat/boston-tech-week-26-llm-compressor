# Infrastructure Status

**Cluster:** OpenShift 4.x  
**Namespace:** `workshop`

---

## Health Checks

### Check Pod Status
```bash
oc get pods -n workshop
```

### Test vLLM Endpoints
```bash
# Original model
curl http://95.133.252.99:8000/v1/models

# Quantized model
curl http://95.133.252.99:8001/v1/models
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
