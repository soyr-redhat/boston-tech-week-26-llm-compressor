# Quick Start - LLM Benchmarking

## Setup (2 minutes)

```bash
# Create and activate virtual environment (recommended)
python3 -m venv guidellm-env
source guidellm-env/bin/activate  # On Windows: guidellm-env\Scripts\activate

# Install guidellm with numpy constraint
pip install 'numpy<2' guidellm

# Set endpoints
export ORIGINAL_API="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
export QUANTIZED_API="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
```

## Quick Test (1 minute)

```bash
# Test original model
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 5
```

## Compare Both Models (3 minutes)

```bash
# Benchmark original
guidellm \
  --target "$ORIGINAL_API" \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 20

# Benchmark quantized
guidellm \
  --target "$QUANTIZED_API" \
  --model "RedHatAI/Qwen3.5-9B-quantized.w4a16" \
  --data-type emulated \
  --emulated-tokens 100 \
  --request-count 20
```

## What to Look For

| Metric | Original | Quantized | Expected |
|--------|----------|-----------|----------|
| Throughput | ? tok/s | ? tok/s | **1.5-2x faster** |
| P50 Latency | ? ms | ? ms | **30-40% lower** |
| P95 Latency | ? ms | ? ms | **30-40% lower** |

## Troubleshooting

**Installation error?**
```bash
python3 -m venv venv && source venv/bin/activate
pip install guidellm
```

**Connection error?**
```bash
# Test with curl
curl $ORIGINAL_API/models
```

**Too slow?**
- Reduce `--request-count` to 5
- Try during a break when fewer people are testing

## Demo UI

Watch the live comparison: https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com

---

**Questions?** Raise your hand or find the instructor
