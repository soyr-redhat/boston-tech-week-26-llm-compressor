---
layout: default
title: Home
---

# Boston Tech Week 2026
## LLM Quantization Workshop

Welcome to the hands-on workshop on LLM quantization and performance benchmarking!

## Quick Links

### For Participants
- **[Quick Start Guide](quick-start)** - Get benchmarking in 2 minutes
- **[Workshop Guide](workshop-guide)** - Full 60-minute workshop agenda
- **[Demo UI](https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com)** - Live model comparison

### For Instructors
- **[Instructor Walkthrough](instructor-guide)** - Step-by-step teaching guide
- **[Cluster Status](cluster-status)** - Infrastructure and management

## Workshop Overview

**Duration:** 60 minutes  
**Format:** Instructor demo (30 min) + Hands-on benchmarking (30 min)

### Part 1: Understanding Quantization (30 min)
- What is quantization and why does it matter?
- Live side-by-side comparison of FP16 vs INT4 models
- Performance metrics and quality trade-offs

### Part 2: Hands-On Benchmarking (30 min)
- Install `guidellm` on your laptop
- Benchmark real production endpoints
- Compare throughput, latency, and quality

## What You'll Learn

1. **Model Quantization Fundamentals**
   - FP16, INT8, INT4, FP8 precision formats
   - Memory and compute trade-offs
   - When to quantize (and when not to)

2. **Performance Benchmarking**
   - Using guidellm to load test LLM APIs
   - Interpreting metrics: throughput, latency, P95/P99
   - Real-world production considerations

3. **Hands-On Experience**
   - Deploy quantized models with vLLM
   - Measure actual speedup (1.5-2x typical)
   - Understand quality vs performance balance

## Prerequisites

- **Laptop** with internet access
- **Python 3.9+** installed
- **Terminal/Command Prompt** access
- No GPU or cluster access required!

## Setup (Before Workshop)

```bash
# Install guidellm (5 seconds)
pip install guidellm

# Verify installation
guidellm --version
```

That's it! The vLLM models are already running in the cloud for you.

## Live Infrastructure

### Model Endpoints (Public)
- **Original Model (FP16):** https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1
- **Quantized Model (INT4):** https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1

### Comparison UI (Demo)
- **URL:** https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
- Side-by-side streaming responses
- Real-time metrics
- Everforest theme

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Your Laptop (50 users)                 │
│                                                          │
│  $ pip install guidellm                                 │
│  $ guidellm --target <endpoint> ...                     │
│                                                          │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             │ HTTPS                      │ HTTPS
             │                            │
       ┌─────▼──────┐             ┌──────▼─────┐
       │  Original  │             │ Quantized  │
       │ Qwen 7B    │             │ Qwen 9B    │
       │ FP16       │             │ INT4       │
       │ 2× L4 GPU  │             │ 2× L4 GPU  │
       └────────────┘             └────────────┘
              OpenShift Cluster
```

## Resources

- **vLLM Documentation:** [docs.vllm.ai](https://docs.vllm.ai/)
- **guidellm GitHub:** [neuralmagic/guidellm](https://github.com/neuralmagic/guidellm)
- **LLM Compressor:** [vllm-project/llm-compressor](https://github.com/vllm-project/llm-compressor)
- **RedHat AI Models:** [huggingface.co/RedHatAI](https://huggingface.co/RedHatAI)

## After the Workshop

- Quantize your own models with `llm-compressor`
- Deploy in production with vLLM
- Experiment with INT8, FP8, structured pruning
- Join the discussion in Boston Tech Week Slack

## Questions?

- Raise your hand during the workshop
- Ask in Boston Tech Week Slack
- Email: workshop@example.com

---

**Ready to get started?** Head to the [Quick Start Guide](quick-start) →
