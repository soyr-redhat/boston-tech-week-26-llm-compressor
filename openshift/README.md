# OpenShift Deployment

Deploy the comparison UI and vLLM models to OpenShift.

## Quick Deploy

```bash
# Create namespace
oc create namespace boston-tech-week-2026

# Create ConfigMap from comparison_ui.py
oc create configmap comparison-ui-code \
  --from-file=comparison_ui.py=../apps/comparison_ui.py \
  -n boston-tech-week-2026

# Deploy vLLM models
oc apply -f deployment-vllm-original.yaml -n boston-tech-week-2026
oc apply -f deployment-vllm-quantized.yaml -n boston-tech-week-2026

# Deploy comparison UI
oc apply -f deployment-comparison-ui.yaml -n boston-tech-week-2026

# Get the route URL
oc get route comparison-ui -n boston-tech-week-2026 -o jsonpath='{.spec.host}'
```

## Check Status

```bash
# Watch deployments
oc get pods -n boston-tech-week-2026 -w

# Check vLLM logs
oc logs -f deployment/vllm-original -n boston-tech-week-2026
oc logs -f deployment/vllm-quantized -n boston-tech-week-2026

# Check UI logs
oc logs -f deployment/comparison-ui -n boston-tech-week-2026
```

## Resource Requirements

Per deployment:
- **vLLM Original:** 1 GPU, 4-8 CPU, 8-16Gi RAM
- **vLLM Quantized:** 1 GPU, 4-8 CPU, 8-16Gi RAM
- **Comparison UI:** 1-2 CPU, 2-4Gi RAM (no GPU needed)

**Total:** 2 GPUs minimum

## Scaling for Workshop

For 50 participants sharing the same models:
```bash
# Single set of models for all users
# They all access the same comparison UI
# No per-user resources needed!
```

## Troubleshooting

**Pods not starting:**
```bash
# Check events
oc describe pod <pod-name> -n boston-tech-week-2026

# Check GPU availability
oc get nodes -o json | jq '.items[].status.allocatable."nvidia.com/gpu"'
```

**Out of GPU memory:**
```bash
# Use smaller models or reduce replicas
# Each vLLM deployment needs ~2-4GB VRAM
```

**UI can't connect to vLLM:**
```bash
# Check services are running
oc get svc -n boston-tech-week-2026

# Test connectivity from UI pod
oc exec -it deployment/comparison-ui -n boston-tech-week-2026 -- \
  curl http://vllm-original:8080/health
```
