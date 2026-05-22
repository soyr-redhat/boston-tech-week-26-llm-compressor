
# Instructor Walkthrough - LLM Quantization Workshop

**Duration:** 60 minutes  
**Audience:** 50 participants  
**Your Role:** Live demo + hands-on facilitation


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
-  Production inference at scale
-  Running bigger models on limited hardware
-  Lowering latency and cost

When NOT to:
-  Critical applications where 1% accuracy matters
-  Fine-tuning (training needs precision)
-  Models that already degrade significantly"

### Wrap Part 1 (5 min)

**Show UI one more time:**

"Notice the quantized model is FASTER even though it has more parameters (9B vs 7B). That's the power of quantization.

Now YOU'RE going to benchmark these models yourselves using guidellm - a tool for load testing LLM APIs."


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


**Remember:**

- Energy and enthusiasm matter more than perfection
- Encourage questions throughout
- Relate to real-world use cases
- Have fun!

 **You're ready. Go show them how quantization works!**
