# Boston Tech Week 2026: LLM Quantization Workshop

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

## Quick Start

### For Workshop Attendees (OpenShift/JupyterHub)

1. Log into your OpenShift user account
2. Launch JupyterHub notebook
3. Clone this repo and run setup:
   ```bash
   git clone https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor.git
   cd boston-tech-week-26-llm-compressor
   ./setup.sh
   ```
4. Open `workshop_notebook.ipynb` and follow along!

## Quick Reference

### Environment Setup
```bash
# Activate environment
source .venv/bin/activate

# Check GPU
nvidia-smi

# Verify CUDA in Python
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Expected Results (Qwen2.5-0.5B)

| Model | Size | Compression | Memory |
|-------|------|-------------|--------|
| FP16 (original) | ~1.0 GB | - | ~2 GB |
| INT8 (quantized) | ~0.5 GB | ~50% | ~1.5 GB |
| INT4 (quantized) | ~0.25 GB | ~75% | ~1 GB |

### Common Commands
```bash
# Watch GPU memory in real-time
watch -n 1 nvidia-smi

# Start Jupyter notebook
jupyter notebook workshop_notebook.ipynb

# Install additional package
uv pip install <package-name>
```

## Repository Contents

- `workshop_notebook.ipynb` - Main hands-on notebook with all exercises
- `setup.sh` - Automated setup script
- `requirements.txt` - Full dependencies for Linux/GPU environments
- `requirements-dev.txt` - Minimal dependencies for local development

## Resources

- [llm-compressor documentation](https://github.com/vllm-project/llm-compressor)
- [vllm documentation](https://github.com/vllm-project/vllm)
- [Qwen2.5-0.5B model card](https://huggingface.co/Qwen/Qwen2.5-0.5B)

## Support

During the workshop, use the designated chat channel for troubleshooting.
