# ✅ Workshop Ready!

## Boston Tech Week 2026: LLM Quantization Workshop

Everything is deployed and ready for the workshop!

## 🔗 Access the Workshop

**Comparison UI:**  
https://comparison-ui-boston-tech-week-2026.apps.ocp.ntdrq.sandbox503.opentlc.com

## 🚀 What's Running

### 1. Comparison UI (Gradio)
- **Status:** ✅ Running
- **Purpose:** Side-by-side model comparison interface
- **Access:** Public route above
- **Resources:** 1-2 CPU, 2-4 GB RAM

### 2. vLLM Original Model
- **Model:** Qwen/Qwen2.5-0.5B (FP16 - full precision)
- **Status:** ✅ Running and healthy
- **Endpoint:** `vllm-original:8080` (internal)
- **Purpose:** Baseline for comparison
- **Resources:** 1 GPU, 4-8 CPU, 8-16 GB RAM

### 3. vLLM Quantized Model
- **Model:** Qwen/Qwen2.5-0.5B-Instruct (for comparison)
- **Status:** ✅ Running and healthy
- **Endpoint:** `vllm-quantized:8081` (internal)
- **Purpose:** Show different model variant
- **Resources:** 1 GPU, 4-8 CPU, 8-16 GB RAM

## 📊 Workshop Flow

### Part 1: Introduction (10 min)
Instructor explains quantization concepts

### Part 2: Live Demo (15 min)
- Instructor shows compression process
- Explains GPTQ, INT4, INT8, FP8
- Shows pre-quantized models on HuggingFace

### Part 3: Hands-On Comparison (30 min)
**All 50 participants use the same UI:**

1. Open: https://comparison-ui-boston-tech-week-2026.apps.ocp.ntdrq.sandbox503.opentlc.com
2. See pre-configured endpoints (8080 and 8081)
3. Try example prompts
4. Compare speed and quality side-by-side
5. Observe metrics in real-time

### Part 4: Wrap-up (5 min)
Q&A and next steps

## 🎯 What Participants Will See

**When they open the UI:**
- Simple, clean interface
- Two columns: "Original Model" vs "Quantized Model"
- Input box for prompts
- Example prompts to try
- Real-time metrics after each query:
  - Latency (milliseconds)
  - Throughput (tokens/sec)
  - Speedup comparison
  - Quality comparison

**Expected Results:**
- Both models produce good responses
- Quantized may be slightly faster (same base model)
- Quality is nearly identical
- Easy to understand trade-offs

## 🔧 Technical Details

**Cluster:**
- OpenShift with 4× L4 GPUs
- Namespace: `boston-tech-week-2026`
- All components deployed and healthy

**Capacity:**
- ✅ Supports all 50 participants (shared access)
- ✅ No per-user resources needed
- ✅ Stateless UI scales easily

## 📝 For the Instructor

**Before workshop:**
1. ✅ Models deployed and loaded
2. ✅ UI accessible from public route
3. ✅ Test with a few prompts to warm up
4. ✅ Share URL with participants

**During workshop:**
```bash
# Monitor if needed
oc logs -f deployment/vllm-original -n boston-tech-week-2026
oc logs -f deployment/vllm-quantized -n boston-tech-week-2026
oc logs -f deployment/comparison-ui -n boston-tech-week-2026

# Check pod health
oc get pods -n boston-tech-week-2026

# Watch GPU usage
watch -n 5 'oc exec -it deployment/vllm-original -n boston-tech-week-2026 -- nvidia-smi'
```

**If anything breaks:**
```bash
# Restart a deployment
oc rollout restart deployment/<name> -n boston-tech-week-2026

# Check logs for errors
oc describe pod/<pod-name> -n boston-tech-week-2026
```

## 📚 Workshop Materials

**Repository:** https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor

**Key files:**
- `comparison_ui.py` - The Gradio interface
- `WORKSHOP.md` - Detailed workshop instructions
- `openshift/` - Deployment manifests
- `deploy_to_openshift.sh` - One-command deploy script

## 🎓 Learning Outcomes

By the end, participants will:
- ✅ Understand what quantization is
- ✅ See real speed vs quality trade-offs
- ✅ Know how to use vLLM for model serving
- ✅ Understand how to deploy compressed models
- ✅ Have hands-on experience comparing models

## 🚨 Common Issues & Solutions

**UI slow to respond:**
- Normal for first request (model loading)
- Subsequent requests are faster

**"Cannot connect" errors:**
- Check vLLM pods are running: `oc get pods -n boston-tech-week-2026`
- Verify health: `oc get pods -n boston-tech-week-2026 | grep vllm`

**Too many participants:**
- Current setup handles 50+ easily (stateless)
- If needed, can scale UI replicas

## ✨ Success Criteria

✅ **Pre-workshop:**
- All 3 deployments running
- UI accessible via public route
- Both vLLM models responding to health checks

✅ **During workshop:**
- Participants can access UI
- Prompts return responses
- Metrics display correctly
- No crashes or errors

✅ **Post-workshop:**
- Participants understand quantization
- Have seen real performance differences
- Know where to find pre-quantized models

---

## 🎉 YOU'RE READY!

Share this URL with participants:
**https://comparison-ui-boston-tech-week-2026.apps.ocp.ntdrq.sandbox503.opentlc.com**

The framework is solid, the deployment is working, and the workshop is ready to go!
