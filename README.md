# Boston Tech Week 2026: LLM Quantization Workshop

Learn how model quantization makes LLMs faster and more efficient through hands-on comparison.

## Workshop Overview

**Duration:** 60 minutes  
**Audience:** ~50 participants  
**Infrastructure:** OpenShift cluster with L4 GPUs

## What You'll Learn

1. What is model quantization and why it matters
2. How quantization reduces model size by 70-75%
3. Real performance comparison: original vs quantized models
4. Deploy models with vLLM for optimized inference

## Workshop Format

### Part 1: Introduction (10 min)
**Presentation:** What is quantization and why it matters
- INT8, INT4, FP8 compression techniques
- Memory, speed, and cost benefits
- Real-world use cases

### Part 2: Understanding Compression (15 min)
**Instructor Demo:** How quantization works
- GPTQ quantization walkthrough
- Trade-offs: size vs quality vs speed
- Pre-quantized models from Red Hat AI / NeuralMagic

### Part 3: Hands-On Comparison (30 min)
**Interactive Exercise:**
- Deploy pre-quantized vLLM models
- Use side-by-side comparison UI
- Compare speed and quality in real-time
- Measure GPU memory savings

### Part 4: Wrap-up (5 min)
- Key takeaways and resources
- Next steps for production deployment

## Quick Start

### For Workshop Participants

**The instructor will provide:**
- Pre-deployed vLLM endpoints (ports 8080 and 8081)
- Access to the comparison UI

**To run locally (optional):**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor.git
   cd boston-tech-week-26-llm-compressor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the comparison UI:**
   ```bash
   python comparison_ui.py
   ```

4. **Open in browser:**
   ```
   http://localhost:7860
   ```

## Using the Comparison UI

### Features

- **Side-by-side comparison** of original vs quantized models
- **Real-time metrics:** latency, throughput, tokens/sec
- **Quality assessment:** compare responses side-by-side
- **Easy configuration:** just specify vLLM ports

### Example Results (Qwen2.5-0.5B)

| Metric | Original (FP16) | Quantized (INT4) | Improvement |
|--------|----------------|------------------|-------------|
| Model Size | ~1.0 GB | ~0.28 GB | 72% smaller |
| VRAM Usage | ~2 GB | ~0.5 GB | 75% less |
| Latency | 120ms | 80ms | 33% faster |
| Throughput | 8.3 tok/s | 12.1 tok/s | 1.46x faster |
| Quality | Baseline | ~99% retained | Minimal loss |

### Deploying vLLM Models (Advanced)

**Original model:**
```bash
vllm serve Qwen/Qwen2.5-0.5B --port 8080
```

**Quantized model:**
```bash
vllm serve neuralmagic/Qwen2.5-0.5B-Instruct-FP8 \
  --port 8081 \
  --quantization fp8
```

**Check GPU usage:**
```bash
nvidia-smi
```

## Repository Contents

- `comparison_ui.py` - Gradio-based comparison interface
- `WORKSHOP.md` - Detailed workshop instructions
- `requirements.txt` - Python dependencies
- `setup.sh` - Environment setup script

## Resources

- [llm-compressor documentation](https://github.com/vllm-project/llm-compressor)
- [vllm documentation](https://github.com/vllm-project/vllm)
- [Qwen2.5-0.5B model card](https://huggingface.co/Qwen/Qwen2.5-0.5B)

## Support

During the workshop, use the designated chat channel for troubleshooting.
