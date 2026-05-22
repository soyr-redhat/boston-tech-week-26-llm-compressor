# Workshop Demo Verification ✅

**Date:** 2026-05-22  
**Event:** Boston Tech Week 2026 - LLM Quantization Workshop

## Infrastructure Status

### vLLM Deployments

✅ **Original Model (FP16)**
- Endpoint: https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1
- Model: `Qwen/Qwen2.5-7B-Instruct`
- Max Context: 8192 tokens
- Status: **RUNNING**
- Test Response: ✅ Verified

✅ **Quantized Model (INT4)**
- Endpoint: https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1
- Model: `RedHatAI/Qwen3.5-9B-quantized.w4a16`
- Max Context: 8192 tokens
- Status: **RUNNING**
- Test Response: ✅ Verified

### Comparison UI

✅ **Instructor Demo Interface**
- URL: https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
- Theme: Everforest (matching instructor's nvim config)
- Features:
  - Side-by-side concurrent comparison
  - Real-time streaming responses
  - Live metrics (latency, throughput)
  - Pre-configured endpoints
- Status: **READY**

## Workshop Architecture

**Capacity:** 50 participants  
**GPU Usage:** 2× L4 GPUs (shared backend)  
**Approach:** Instructor demo + participant benchmarking

### Part 1: Demo (30 min)
- Instructor uses comparison UI at user1 URL
- Live demonstration of quantization benefits
- Participants observe and learn

### Part 2: Hands-On (30 min)
- Participants install `guidellm` on their laptops
- Benchmark both models from their own machines
- Compare metrics and discuss results

## Pre-Workshop Checklist

### Infrastructure
- [x] Original vLLM deployed and accessible
- [x] Quantized vLLM deployed and accessible
- [x] Comparison UI deployed and accessible
- [x] Public routes configured with TLS
- [x] Both models tested with curl
- [x] UI tested with real prompts

### Documentation
- [x] WORKSHOP_GUIDE.md complete
- [x] Installation instructions for guidellm
- [x] Example benchmark commands
- [x] Expected metrics documented
- [x] Troubleshooting section

### Verification Tests

```bash
# Test 1: Check model endpoints
curl -s https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models
curl -s https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models

# Test 2: Run completion
curl -X POST https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "prompt": "Test prompt",
    "max_tokens": 20
  }'

# Test 3: Access UI
open https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
```

## Day-Of Setup

### 15 Minutes Before
1. Verify both vLLM pods are running: `oc get pods -n workshop`
2. Check logs for errors: `oc logs -f deployment/vllm-original -n workshop`
3. Test UI in browser
4. Run one full comparison to warm up models

### During Workshop
1. Share comparison UI link: https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
2. Demonstrate concurrent execution
3. Show metrics and speedup
4. Share API endpoints for participant benchmarking:
   - Original: https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1
   - Quantized: https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1

## Resource Usage

### Current
- GPUs: 2/4 L4 GPUs used
- CPU: ~6 cores
- RAM: ~12GB
- Storage: ~40GB (model weights)

### Headroom
- 2 additional GPUs available
- Can handle load from 50 concurrent guidellm users
- API endpoints publicly accessible

## Backup Plans

### If UI fails
- Use curl commands to demonstrate API
- Share screen showing raw JSON responses
- Participants can still benchmark

### If one model fails
- Continue with working model
- Explain quantization theory
- Show historical benchmark results

### If guidellm doesn't work for participants
- Provide pre-run benchmark results
- Use curl with time measurement
- Focus on demo portion

## Contact

**Cluster:** https://console-openshift-console.apps.ocp.ntdrq.sandbox503.opentlc.com  
**Namespace:** workshop  
**Admin Access:** Already logged in via `oc`

---

**Status:** ✅ READY FOR WORKSHOP
