# Quick Start: Deploy to OpenShift

Complete deployment guide for the Boston Tech Week 2026 workshop on OpenShift.

## Prerequisites

- OpenShift cluster with GPU nodes (L4 or better)
- Cluster admin access
- `oc` CLI configured and logged in

## One-Command Deploy

```bash
# Deploy everything
./deploy_to_openshift.sh
```

## Manual Deployment

### Step 1: Create Namespace

```bash
oc create namespace boston-tech-week-2026
```

### Step 2: Deploy vLLM Models

```bash
# Original model (FP16)
oc apply -f openshift/deployment-vllm-original.yaml -n boston-tech-week-2026

# Quantized model (FP8)
oc apply -f openshift/deployment-vllm-quantized.yaml -n boston-tech-week-2026
```

### Step 3: Create ConfigMap for UI Code

```bash
oc create configmap comparison-ui-code \
  --from-file=comparison_ui.py \
  -n boston-tech-week-2026
```

### Step 4: Deploy Comparison UI

```bash
oc apply -f openshift/deployment-comparison-ui.yaml -n boston-tech-week-2026
```

### Step 5: Get Access URL

```bash
# Get the route
oc get route comparison-ui -n boston-tech-week-2026

# Or get just the URL
echo "https://$(oc get route comparison-ui -n boston-tech-week-2026 -o jsonpath='{.spec.host}')"
```

## Verify Deployment

### Check Pods

```bash
oc get pods -n boston-tech-week-2026

# Expected output:
# NAME                              READY   STATUS    RESTARTS   AGE
# vllm-original-xxx                 1/1     Running   0          2m
# vllm-quantized-xxx                1/1     Running   0          2m
# comparison-ui-xxx                 1/1     Running   0          1m
```

### Check vLLM Health

```bash
# Port-forward to test locally
oc port-forward svc/vllm-original 8080:8080 -n boston-tech-week-2026 &
oc port-forward svc/vllm-quantized 8081:8081 -n boston-tech-week-2026 &

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8081/health

# Kill port-forwards
pkill -f "port-forward.*vllm"
```

### Check UI

```bash
# Get logs
oc logs -f deployment/comparison-ui -n boston-tech-week-2026

# Should see:
# Running on public URL: https://...
```

## Workshop Day Setup

### Before Workshop (30 min before)

1. **Deploy models:**
   ```bash
   oc apply -f openshift/ -n boston-tech-week-2026
   ```

2. **Wait for models to load** (~2-3 minutes):
   ```bash
   oc logs -f deployment/vllm-original -n boston-tech-week-2026
   oc logs -f deployment/vllm-quantized -n boston-tech-week-2026
   ```

3. **Get participant URL:**
   ```bash
   oc get route comparison-ui -n boston-tech-week-2026 -o jsonpath='{.spec.host}'
   ```

4. **Share URL with participants**

### During Workshop

All 50 participants use the **same URL** - no per-user deployment needed!

The UI is stateless, so multiple users can access simultaneously.

### Monitor During Workshop

```bash
# Watch GPU usage
watch -n 5 'oc get pods -n boston-tech-week-2026 -o wide'

# Check vLLM logs for errors
oc logs -f deployment/vllm-original -n boston-tech-week-2026
oc logs -f deployment/vllm-quantized -n boston-tech-week-2026
```

## Resource Usage

**Minimum Requirements:**
- 2 GPUs (1 for original, 1 for quantized)
- 16 CPU cores
- 32 GB RAM

**Current Cluster:**
- 4× L4 GPUs (23GB each)
- Can support workshop with capacity to spare

## Troubleshooting

### Pods stuck in Pending

```bash
# Check events
oc describe pod <pod-name> -n boston-tech-week-2026

# Common issue: No GPU available
# Solution: Check GPU node availability
oc get nodes -o json | jq '.items[] | select(.metadata.labels."nvidia.com/gpu.count" != null) | {name: .metadata.name, gpus: .metadata.labels."nvidia.com/gpu.count", allocatable: .status.allocatable."nvidia.com/gpu"}'
```

### vLLM taking too long to load

Normal! Model loading takes 1-3 minutes. Watch logs:
```bash
oc logs deployment/vllm-original -n boston-tech-week-2026 --tail=50 -f
```

### UI can't connect to vLLM

The UI needs to connect via service names. Update `comparison_ui.py` ports:
- Original: `vllm-original:8080` (or just `8080` if using localhost)
- Quantized: `vllm-quantized:8081` (or just `8081` if using localhost)

### Out of Memory

Reduce model size or use smaller models:
```bash
# Edit deployment and change model
oc edit deployment vllm-original -n boston-tech-week-2026
# Change to: Qwen/Qwen2.5-0.5B (already the smallest)
```

## Cleanup

```bash
# Delete everything
oc delete namespace boston-tech-week-2026

# Or individual components
oc delete -f openshift/ -n boston-tech-week-2026
```

## Next Steps

After successful deployment:
1. Test the UI with example prompts
2. Verify both models respond correctly
3. Share the URL with participants
4. Prepare backup plan (pre-recorded demo) in case of issues
