# Quick Start - LLM Benchmarking

## Setup (1 minute)

**Mac/Linux:**
```bash
curl -sSL https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/install.ps1 | iex
```

The script will install guidellm and show you the next steps.

## Quick Test (1 minute)

```bash
# Set endpoints (if not already done)
export ORIGINAL_API="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
export QUANTIZED_API="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"

# Test original model
guidellm benchmark \
  --target "$ORIGINAL_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 5
```

## Compare Both Models (3 minutes)

```bash
# Benchmark original
guidellm benchmark \
  --target "$ORIGINAL_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 20

# Benchmark quantized
guidellm benchmark \
  --target "$QUANTIZED_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 20
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
# Manual install as fallback
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
