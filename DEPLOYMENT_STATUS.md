# Deployment Status

## ✅ Working Components

### Comparison UI
- **Status:** ✅ Running
- **URL:** https://comparison-ui-boston-tech-week-2026.apps.ocp.ntdrq.sandbox503.opentlc.com
- **Pod:** Running successfully
- **Access:** Public via route

### vLLM Original Model
- **Status:** ✅ Running
- **Model:** Qwen/Qwen2.5-0.5B (FP16)
- **Port:** 8080
- **Endpoint:** `vllm-original:8080`
- **Pod:** Healthy and passing health checks

### vLLM Quantized Model
- **Status:** ⚠️ Troubleshooting
- **Model:** neuralmagic/Qwen2.5-0.5B-Instruct-FP8
- **Port:** 8081
- **Issue:** Investigating startup issues

## Quick Access

**For Workshop Participants:**
1. Open: https://comparison-ui-boston-tech-week-2026.apps.ocp.ntdrq.sandbox503.opentlc.com
2. Original model endpoint: `vllm-original:8080`
3. Quantized model endpoint: `vllm-quantized:8081` (when ready)

## Current Setup

- **Namespace:** boston-tech-week-2026
- **Cluster:** OpenShift with 4× L4 GPUs
- **Resources:** 2 GPUs allocated (1 per vLLM instance)

## Next Steps

1. ✅ Fix quantized model deployment
2. ✅ Test complete workflow
3. ✅ Create final documentation
4. ✅ Workshop ready!
