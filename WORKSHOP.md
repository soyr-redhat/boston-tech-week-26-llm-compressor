# Boston Tech Week 2026: LLM Quantization Workshop

## Workshop Overview (60 minutes)

**Goal:** Learn how model quantization makes LLMs faster and more efficient through hands-on comparison.

## Workshop Flow

### Part 1: Introduction (10 min)
- What is quantization?
- Why compress models? (memory, speed, cost)
- Demo: Side-by-side comparison of FP16 vs INT4 models

### Part 2: Understanding Compression (15 min)
**Lecture/Demo by Instructor:**
- How GPTQ quantization works
- Trade-offs: size vs quality vs speed
- Tools: llm-compressor, vLLM
- Pre-quantized models on HuggingFace

**Key Concepts:**
- FP16: Full precision (16-bit floats) - slower, larger
- INT8: 8-bit integers - ~50% compression
- INT4: 4-bit integers - ~75% compression
- Quality retention: modern quantization preserves 95-99% of quality

### Part 3: Hands-On Comparison (30 min)

**Each participant will:**

1. **Deploy a pre-quantized model from Red Hat AI**
   - Use vLLM to serve a quantized model
   - Already compressed and ready to use!

2. **Run the comparison UI**
   - Side-by-side chat interface
   - Compare original vs quantized model
   - Measure real speed differences

3. **Experiment with prompts**
   - Test different types of queries
   - Observe quality vs speed trade-offs
   - Check GPU memory usage

### Part 4: Wrap-up (5 min)
- Key takeaways
- Resources for further learning
- Q&A

## Hands-On Instructions

### Step 1: Deploy Your vLLM Model

**Option A: Use instructor-provided endpoints**
```
Original Model:  localhost:8080
Quantized Model: localhost:8081
```

**Option B: Deploy your own (if time permits)**
```bash
# Terminal 1: Original model
vllm serve Qwen/Qwen2.5-0.5B --port 8080

# Terminal 2: Quantized model  
vllm serve neuralmagic/Qwen2.5-0.5B-Instruct-FP8 --port 8081 --quantization fp8
```

### Step 2: Launch the Comparison UI

```bash
python comparison_ui.py
```

Open in your browser: `http://localhost:7860`

### Step 3: Compare Models

1. Enter the vLLM ports (8080 and 8081)
2. Type a prompt or use an example
3. Click "Compare Models"
4. Observe:
   - Response quality (nearly identical)
   - Speed difference (1.3-2x faster)
   - Latency reduction (30-50% less)

### Step 4: Check GPU Memory

```bash
# In another terminal
watch -n 1 nvidia-smi
```

**You'll see:**
- Original model: ~2 GB VRAM
- Quantized model: ~0.5 GB VRAM
- **75% memory savings!**

## Example Prompts to Try

1. **Simple completion:**
   - "The future of artificial intelligence is"
   
2. **Code generation:**
   - "Write a Python function to calculate fibonacci numbers"

3. **Explanation:**
   - "Explain quantum computing in simple terms"

4. **Reasoning:**
   - "What are the benefits of model quantization?"

5. **Creative:**
   - "Tell me a short story about a robot learning to paint"

## What You'll Learn

✅ How quantization reduces model size by 70-75%
✅ Speed improvements of 1.3-2x with minimal quality loss
✅ Practical deployment with vLLM
✅ Trade-offs between compression and quality
✅ How to use pre-quantized models from HuggingFace

## Resources

- **vLLM Documentation:** https://docs.vllm.ai/
- **llm-compressor:** https://github.com/vllm-project/llm-compressor
- **Red Hat AI Models:** https://huggingface.co/RedHatAI
- **neuralmagic Models:** https://huggingface.co/neuralmagic

## Troubleshooting

**UI won't connect to vLLM:**
```bash
# Check if vLLM is running
curl http://localhost:8080/health
curl http://localhost:8081/health
```

**Out of memory:**
- Close other GPU applications
- Use smaller models
- Reduce `max_tokens` in the UI

**Slow responses:**
- Normal! First request loads the model
- Subsequent requests are faster
- Check GPU usage with `nvidia-smi`

## Next Steps

After the workshop:
- Try larger models (1.5B, 3B parameters)
- Experiment with different quantization methods (GPTQ, AWQ, FP8)
- Deploy your own quantized models in production
- Measure quality impact with benchmarks
