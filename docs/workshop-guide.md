
# Boston Tech Week 2026 - LLM Quantization Workshop

## Workshop Overview

In this hands-on workshop, you'll learn about LLM quantization and benchmark real models to measure the performance improvements.

**Duration:** 60 minutes  
**Format:** Instructor-led demo + hands-on benchmarking


## Part 2: Hands-On Benchmarking with guidellm (30 min)

Now **you** will benchmark these models using `guidellm` - a tool for load testing LLM APIs.

### Setup (5 min)

#### Install guidellm

```bash
pip install guidellm
```

#### Model Endpoints

```bash
# Original Model (FP16)
export ORIGINAL_API="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"

# Quantized Model (INT4)
export QUANTIZED_API="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
```

### Benchmark Tasks

#### Task 1: Single-User Latency Test (5 min)

Test how fast each model responds to a single user:

```bash
# Benchmark original model
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 10

# Benchmark quantized model
guidellm \
  --target "$QUANTIZED_API" \
  --model "RedHatAI/Qwen3.5-9B-quantized.w4a16" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 10
```

**Expected Results:**
- Quantized should be **1.5-2x faster** throughput
- Quantized should have **30-40% lower latency**

#### Task 2: Multi-User Load Test (10 min)

See how the models perform under concurrent load:

```bash
# Original model under load
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 50 \
  --max-concurrency 5

# Quantized model under load
guidellm \
  --target "$QUANTIZED_API" \
  --model "RedHatAI/Qwen3.5-9B-quantized.w4a16" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 50 \
  --max-concurrency 5
```

**What to observe:**
- Throughput (requests/sec)
- P50/P95/P99 latency
- Queue times

#### Task 3: Real Prompts (10 min)

Create a `prompts.txt` file:

```text
Explain quantum computing in simple terms
Write a Python function to reverse a string
What are the benefits of LLM quantization?
```

Benchmark with real prompts:

```bash
# Original model
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type file \
  --data "prompts.txt" \
  --max-concurrency 3

# Quantized model
guidellm \
  --target "$QUANTIZED_API" \
  --model "RedHatAI/Qwen3.5-9B-quantized.w4a16" \
  --data-type file \
  --data "prompts.txt" \
  --max-concurrency 3
```


## Discussion Questions

1. **When would you NOT want to quantize?**
   - Critical applications where quality matters more than speed
   - Already fast enough models
   - Models that degrade significantly when quantized

2. **What quantization level should you choose?**
   - INT8: Safest, minimal degradation
   - INT4: Maximum speedup, slight quality loss
   - FP8: Good middle ground for newer GPUs

3. **How does load affect quantized models?**
   - Both models slow down under load
   - Quantized models handle more concurrent requests
   - Memory efficiency = more batch throughput


## Resources

- **vLLM Documentation:** https://docs.vllm.ai/
- **guidellm Documentation:** https://github.com/neuralmagic/guidellm
- **LLM Compressor:** https://github.com/vllm-project/llm-compressor
- **RedHat AI Models:** https://huggingface.co/RedHatAI


## Next Steps

- Try quantizing your own models with `llm-compressor`
- Deploy quantized models in production with vLLM
- Benchmark different quantization levels (INT8 vs INT4 vs FP8)
- Explore structured pruning + quantization for even more gains

**Questions?** Ask in the Boston Tech Week Slack or email workshop@example.com
