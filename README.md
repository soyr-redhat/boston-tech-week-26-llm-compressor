# MIT Build & Brew: LLM Quantization Workshop

Hands-on workshop for quantizing and deploying LLMs using `llm-compressor` and `vllm`.

## Workshop Overview

**Duration:** 60 minutes  
**Audience:** ~50 participants  
**Infrastructure:** OpenShift cluster with L40S GPUs, pre-provisioned user accounts

## What You'll Learn

1. What is model quantization and why it matters
2. How to quantize models using llm-compressor
3. Compare quantized vs original models
4. Deploy with vllm for optimized inference

## Model

We'll use [Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) - small enough to quantize quickly (~2-5 min), but demonstrates real compression benefits.

## Workshop Structure

### Part 1: Introduction (5 min)
- What is quantization? (INT8, INT4, GPTQ)
- Why compress models? (memory, throughput, cost)
- The goal: Quantize Qwen2.5-0.5B and measure the impact

### Part 2: One-Shot Quantization (10 min)
- Run basic quantization script
- Observe model size reduction
- Understand what happened

### Part 3: Deep Dive (20 min)
- Explore llm-compressor configuration
- Try different quantization schemes
- Compare metrics (perplexity, size)

### Part 4: Deploy with vllm (20 min)
- Load original vs quantized model
- Benchmark throughput and latency
- Analyze memory usage

### Part 5: Q&A (5 min)

## Prerequisites

### For Workshop (Required)
- Linux environment with CUDA-capable GPU (L40S)
- OpenShift user account with JupyterHub access
- Python 3.10+

### For Local Development (Optional)
- macOS/Linux with Python 3.10+
- Dev dependencies only (no GPU required for viewing materials)

## Quick Start

### For Workshop Attendees (OpenShift/JupyterHub)

1. Log into your OpenShift user account
2. Launch JupyterHub notebook
3. Clone this repo and run setup:
   ```bash
   git clone https://github.com/soyr-redhat/MIT-build-n-brew-llm-compressor.git
   cd MIT-build-n-brew-llm-compressor
   ./setup.sh
   ```
4. Open `workshop_notebook.ipynb` and follow along!

### For Local Development

**Note:** Full workshop requires Linux with CUDA GPUs. On macOS, only dev dependencies will be installed for viewing materials.

```bash
# Clone the repository
git clone https://github.com/soyr-redhat/MIT-build-n-brew-llm-compressor.git
cd MIT-build-n-brew-llm-compressor

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run setup script (auto-detects platform)
./setup.sh

# Activate environment
source .venv/bin/activate

# Start Jupyter
jupyter notebook workshop_notebook.ipynb
```

On **Linux with CUDA**, the script installs full dependencies (llmcompressor, vLLM).  
On **macOS**, it installs minimal dev dependencies for reviewing materials only.

## Repository Contents

- `workshop_notebook.ipynb` - Main hands-on notebook
- `scripts/` - Helper scripts for quantization and benchmarking
- `configs/` - Sample llm-compressor configurations
- `checkpoints/` - Pre-quantized models (backup)

## Resources

- [llm-compressor documentation](https://github.com/vllm-project/llm-compressor)
- [vllm documentation](https://github.com/vllm-project/vllm)
- [Qwen2.5-0.5B model card](https://huggingface.co/Qwen/Qwen2.5-0.5B)

## Support

During the workshop, use the designated chat channel for troubleshooting.
