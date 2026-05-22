# Boston Tech Week 2026 - LLM Quantization Workshop

## Workshop Overview

In this hands-on workshop, you'll learn about LLM quantization and benchmark real models to measure the performance improvements.

**Duration:** 60 minutes  
**Format:** Instructor-led demo + hands-on benchmarking

---

## Part 1: Understanding Quantization (30 min)

### What is Quantization?

Model quantization reduces the precision of model weights to make inference faster and more memory-efficient:

- **FP16/BF16** (16-bit floating point) - Standard precision
- **FP8** (8-bit floating point) - 2x memory reduction
- **INT8** (8-bit integer) - 2x memory reduction, faster compute
- **INT4** (4-bit integer) - 4x memory reduction, much faster

### Why Quantize?

1. **Faster inference** - 1.5-2.5x throughput improvement
2. **Lower memory** - 2-4x VRAM reduction (fit bigger models)
3. **Lower latency** - 30-50% faster response times
4. **Minimal quality loss** - Typically <2% degradation

### Live Demo

Watch as we:
1. Show the quantization process with `llm-compressor`
2. Deploy two models side-by-side:
   - **Original:** Qwen2.5-7B-Instruct (FP16) - ~20GB VRAM
   - **Quantized:** Qwen3.5-9B-quantized (INT4) - ~19GB VRAM
3. Compare outputs in the web UI

**Demo URL:** https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com

---

## Part 2: Hands-On Benchmarking with guidellm (30 min)

Now **you** will benchmark these models using `guidellm` - a tool for load testing LLM APIs.

### Setup (5 min)

#### Install guidellm

**One-line installer (recommended for all users):**

**Mac/Linux:**
```bash
curl -sSL https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/scripts/install.ps1 | iex
```

The installer will:
- Detect your system
- Install guidellm with the best method available
- Test the installation
- Show you the next steps

**Manual installation (if the script doesn't work):**

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
# Create directories for results
mkdir -p original quantized

# Benchmark original model
cd original
guidellm benchmark \
  --target "$ORIGINAL_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 10
cd ..

# Benchmark quantized model
cd quantized
guidellm benchmark \
  --target "$QUANTIZED_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 10
cd ..
```

**Compare the Results:**

Look at the terminal output summary, or open the HTML reports:
```bash
# View visual reports
open original/benchmarks.html
open quantized/benchmarks.html

# Or compare CSV data
echo "Original:" && tail -1 original/benchmarks.csv
echo "Quantized:" && tail -1 quantized/benchmarks.csv
```

**Expected Results:**
- Quantized should be **1.5-2x faster** throughput
- Quantized should have **30-40% lower latency**

#### Task 2: Multi-User Load Test (10 min)

See how the models perform under concurrent load:

```bash
# Original model under load
cd original
guidellm benchmark \
  --target "$ORIGINAL_API" \
  --profile concurrent \
  --rate 5 \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 50
cd ..

# Quantized model under load
cd quantized
guidellm benchmark \
  --target "$QUANTIZED_API" \
  --profile concurrent \
  --rate 5 \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 50
cd ..
```

**Compare the Results:**

```bash
# View the latest HTML reports
open original/benchmarks.html
open quantized/benchmarks.html
```

**What to observe:**
- Throughput (requests/sec or tokens/sec)
- P50/P95/P99 latency
- How performance degrades under load

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
cd original
guidellm benchmark \
  --target "$ORIGINAL_API" \
  --profile concurrent \
  --rate 3 \
  --data "../prompts.txt"
cd ..

# Quantized model
cd quantized
guidellm benchmark \
  --target "$QUANTIZED_API" \
  --profile concurrent \
  --rate 3 \
  --data "../prompts.txt"
cd ..
```

**Compare Quality + Performance:**

```bash
# View detailed reports
open original/benchmarks.html
open quantized/benchmarks.html
```

Notice: the quantized model is faster AND produces similar quality responses!

---

## Key Metrics to Compare

| Metric | What it Means | Expected Improvement |
|--------|---------------|---------------------|
| **Throughput** | Requests/sec or tokens/sec | 1.5-2x faster |
| **P50 Latency** | Median response time | 30-40% lower |
| **P95 Latency** | 95th percentile (worst 5%) | 30-40% lower |
| **Time to First Token** | How fast generation starts | Similar |
| **VRAM Usage** | Memory consumed | 50-75% less |

---

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

---

## Troubleshooting

### guidellm Installation Issues

**If the one-liner installer fails:**

Try manual installation:

```bash
pip install guidellm
```

**If you see numpy compatibility errors:**

```bash
pip install 'numpy<2' --force-reinstall
pip install guidellm
```

**Verify installation:**

```bash
guidellm --help
```

If you see help text, you're ready to go!

### Connection Errors

If guidellm cannot reach the endpoints:

1. **Check your internet connection** - endpoints are publicly accessible
2. **Verify URLs** - make sure you're using the full HTTPS URLs
3. **Try curl first**:
   ```bash
   curl https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models
   ```
4. **Check firewall** - some corporate networks block external API access

### Slow Responses

If models are responding slowly:

- **Expected under load** - 50 participants sharing 2 models
- **Try different times** - benchmark during demo breaks
- **Reduce request count** - use `--request-count 3` for quick tests
- **Check load** - others may be benchmarking simultaneously

### Alternative Testing (No guidellm)

If guidellm doesn't work, use curl with timing:

```bash
# Time a single request
time curl -X POST https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "prompt": "Explain quantum computing",
    "max_tokens": 100
  }'
```

---

## Resources

- **vLLM Documentation:** https://docs.vllm.ai/
- **guidellm Documentation:** https://github.com/neuralmagic/guidellm
- **LLM Compressor:** https://github.com/vllm-project/llm-compressor
- **RedHat AI Models:** https://huggingface.co/RedHatAI

---

## Cleanup

After the workshop, you can uninstall guidellm:

```bash
pip uninstall guidellm
```

---

## Next Steps

- Try quantizing your own models with `llm-compressor`
- Deploy quantized models in production with vLLM
- Benchmark different quantization levels (INT8 vs INT4 vs FP8)
- Explore structured pruning + quantization for even more gains

**Questions?** Ask in the Boston Tech Week Slack or email workshop@example.com
