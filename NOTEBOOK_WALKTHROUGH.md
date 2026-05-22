# Instructor Walkthrough - LLM Quantization Workshop

**Duration:** 60 minutes  
**Audience:** 50 participants  
**Your Role:** Live demo + hands-on facilitation

---

## Pre-Workshop (15 min before)

### 1. Verify Infrastructure

```bash
# Check pods are running
oc get pods -n workshop-user1

# Should see:
# vllm-original-xxx         1/1     Running
# vllm-quantized-xxx        1/1     Running
# comparison-ui-xxx         1/1     Running

# Check logs for errors
oc logs deployment/vllm-original -n workshop-user1 --tail=20
oc logs deployment/vllm-quantized -n workshop-user1 --tail=20
```

### 2. Test Comparison UI

Open: https://user1-comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com

- Try example prompt
- Verify both models respond
- Check metrics display
- Confirm speedup visible

### 3. Warm Up Models

Run 2-3 test prompts to load models into memory.

---

## Part 1: Theory + Live Demo (30 min)

### Opening (5 min)

**Share screen with comparison UI**

"Welcome! Today we're exploring LLM quantization - making AI models faster without losing quality. I'm going to show you two models side-by-side:

- **Left:** Original Qwen 2.5 (7B parameters, FP16)
- **Right:** Quantized Qwen 3.5 (9B parameters, INT4)

The quantized model is actually BIGGER but uses 4-bit weights instead of 16-bit."

### Live Comparison (10 min)

**Use these prompts in order:**

1. **Short generation:**
   ```
   Explain LLM quantization in one sentence
   ```
   - Point out concurrent execution
   - Show metrics: latency, throughput
   - Highlight speedup

2. **Longer generation:**
   ```
   Write a Python function to calculate fibonacci numbers
   ```
   - Emphasize real-time streaming
   - Compare quality - should be nearly identical
   - Show tokens/sec advantage

3. **Creative task:**
   ```
   Write a haiku about artificial intelligence
   ```
   - Demonstrate quality is preserved
   - Ask audience: "Can you tell which is quantized?"

### Theory Deep Dive (10 min)

**While last prompt is running, explain:**

#### What is Quantization?

"Quantization reduces numeric precision of model weights:

- **FP16** (16-bit float): 2 bytes per weight
- **INT8** (8-bit integer): 1 byte per weight (50% smaller)
- **INT4** (4-bit integer): 0.5 bytes per weight (75% smaller)

A 7B parameter model:
- FP16: ~14 GB VRAM
- INT4: ~3.5 GB VRAM

This isn't just storage - it affects:
- Memory bandwidth (faster)
- Compute throughput (more ops/sec)
- Cache efficiency (more fits in L1/L2)"

#### Why It Works

"Neural networks are remarkably robust to precision loss:

1. **Weights cluster** - many similar values round to same number
2. **Not all weights matter equally** - some are more important
3. **Inference is forgiving** - training needs precision, inference doesn't

Typical quality loss: <2% degradation in benchmarks"

#### Trade-offs

"When to quantize:
- ✅ Production inference at scale
- ✅ Running bigger models on limited hardware
- ✅ Lowering latency and cost

When NOT to:
- ❌ Critical applications where 1% accuracy matters
- ❌ Fine-tuning (training needs precision)
- ❌ Models that already degrade significantly"

### Wrap Part 1 (5 min)

**Show UI one more time:**

"Notice the quantized model is FASTER even though it has more parameters (9B vs 7B). That's the power of quantization.

Now YOU'RE going to benchmark these models yourselves using guidellm - a tool for load testing LLM APIs."

---

## Part 2: Hands-On Benchmarking (30 min)

### Setup (5 min)

**Share screen with terminal**

```bash
# Install guidellm
pip install guidellm

# Set endpoints
export ORIGINAL_API="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
export QUANTIZED_API="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
```

"These are the same models you just saw. Now you'll programmatically benchmark them from your laptops."

### Task 1: Quick Test (5 min)

**Run this together:**

```bash
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 5
```

**While running, explain:**

"guidellm is sending 5 test requests, each asking for 100 tokens. Watch the metrics:

- **Throughput:** requests or tokens per second
- **Latency:** P50 (median), P95 (95th percentile)
- **Time to First Token:** How fast generation starts"

**After results:**

"Now try the quantized model - change the target and model name. You should see ~1.5-2x improvement."

### Task 2: Load Test (10 min)

**Increase the difficulty:**

```bash
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 50 \
  --max-concurrency 5
```

"Now we're simulating 50 requests with 5 concurrent users. This is closer to production load.

**What to observe:**
- Queue times increase
- P95 latency gets worse (tail latency)
- Throughput hits a ceiling

The quantized model should handle load better due to faster processing."

**Walk around and help participants with errors.**

### Task 3: Real Prompts (10 min)

"Let's test with actual prompts instead of emulated tokens."

**Create prompts.txt:**

```text
Explain quantum computing in simple terms
Write a Python function to reverse a string
What are the benefits of LLM quantization?
Describe how neural networks work
Generate a creative story about robots
```

```bash
guidellm \
  --target "$QUANTIZED_API" \
  --model "RedHatAI/Qwen3.5-9B-quantized.w4a16" \
  --data-type file \
  --data "prompts.txt" \
  --max-concurrency 3
```

"Notice the variability - some prompts generate more, some less. This is real-world behavior."

### Wrap Part 2 (5 min)

**Recap key learnings:**

"What did you discover?

- Quantized models are consistently faster (1.5-2x throughput)
- Latency is lower (30-40% reduction)
- Quality is nearly identical
- Under load, the advantage grows

This is why companies like Meta, OpenAI, and Anthropic use quantization in production."

---

## Discussion & Q&A (5 min)

**Prompt audience:**

1. "When would you NOT want to quantize a model?"
   - Critical applications (medical, legal)
   - Already fast enough
   - Fine-tuning scenarios

2. "What quantization level should you choose?"
   - INT8: Safest, minimal loss
   - INT4: Maximum speedup, slight loss
   - FP8: Good for newer GPUs

3. "How does load affect quantized models?"
   - Both slow down under load
   - Quantized models degrade more gracefully
   - Memory efficiency = more batch throughput

---

## Common Questions

**Q: Can I quantize any model?**  
A: Most yes, but check HuggingFace for pre-quantized versions first. Quantizing yourself requires the full model in memory.

**Q: What about FP8?**  
A: Newer format, good for H100/H200 GPUs. INT4 is more mature and widely supported.

**Q: Does quantization affect fine-tuning?**  
A: Generally train in FP16/BF16, then quantize for inference. QLoRA allows quantized fine-tuning but it's slower.

**Q: How do I quantize my own model?**  
A: Use `llm-compressor` (from vLLM team) or similar tools. Check the resources section for links.

**Q: What about smaller models like 1B params?**  
A: Quantization helps less at smaller sizes. Focus on 7B+ models.

---

## Post-Workshop

### Share Resources

- **Slides/Code:** [Your GitHub repo]
- **guidellm:** https://github.com/neuralmagic/guidellm
- **LLM Compressor:** https://github.com/vllm-project/llm-compressor
- **vLLM Docs:** https://docs.vllm.ai/
- **RedHat AI Models:** https://huggingface.co/RedHatAI

### Encourage Next Steps

"Try this yourself:
1. Deploy a vLLM instance on your cloud provider
2. Load a quantized model from HuggingFace
3. Benchmark with guidellm
4. Compare cost and performance

Start with small models (1-3B) to learn, then scale to production."

---

## Troubleshooting Tips

### If UI is slow
- Too many people using it simultaneously
- Switch to terminal demos only
- Use curl for raw API calls

### If guidellm fails for participants
- Check Python version (3.9+)
- Suggest virtual environment
- Fallback to curl with timing
- Share your benchmark results

### If models crash
- Check pod logs: `oc logs deployment/vllm-original -n workshop-user1`
- Out of memory? Restart: `oc rollout restart deployment/vllm-original -n workshop-user1`
- Show pre-recorded results as backup

### If endpoints are unreachable
- Verify routes: `oc get routes -n workshop-user1`
- Check network policies
- Use instructor laptop as proxy

---

**Remember:**

- Energy and enthusiasm matter more than perfection
- Encourage questions throughout
- Relate to real-world use cases
- Have fun!

🚀 **You're ready. Go show them how quantization works!**
