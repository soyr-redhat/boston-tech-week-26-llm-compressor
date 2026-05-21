# Quick Reference Guide

## Environment Setup

### Using uv (recommended)
```bash
# One-time setup
./setup.sh

# Activate environment
source .venv/bin/activate
```

### Manual setup
```bash
# Create venv with uv
uv venv

# Install dependencies
source .venv/bin/activate
uv pip install -e .
```

### Add new package
```bash
uv pip install <package-name>
```

---

## Command Line Quantization

### Quantize to INT4
```bash
python scripts/quantize_qwen.py \
    --model Qwen/Qwen2.5-0.5B \
    --bits 4 \
    --output ./qwen2.5-0.5b-gptq-int4 \
    --num-samples 256
```

### Quantize to INT8
```bash
python scripts/quantize_qwen.py \
    --model Qwen/Qwen2.5-0.5B \
    --bits 8 \
    --output ./qwen2.5-0.5b-gptq-int8 \
    --num-samples 256
```

## Benchmarking with vLLM

```bash
python scripts/benchmark_vllm.py \
    --original Qwen/Qwen2.5-0.5B \
    --quantized ./qwen2.5-0.5b-gptq-int4 \
    --num-prompts 50
```

## Python API Examples

### Load and Test Model
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-0.5B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype="auto"
)

# Generate
inputs = tokenizer("The future of AI is", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

### Quantize with llm-compressor
```python
from llmcompressor.transformers import oneshot
from datasets import load_dataset

# Recipe
recipe = """
quant_stage:
    quant_modifiers:
        GPTQModifier:
            sequential_update: false
            ignore: ["lm_head"]
            config_groups:
                group_0:
                    weights:
                        num_bits: 4
                        type: "int"
                        symmetric: true
                        strategy: "channel"
                    targets: ["Linear"]
"""

# Calibration data
dataset = load_dataset(
    "allenai/c4",
    data_files="en/c4-train.00000-of-01024.json.gz",
    split="train"
).select(range(256))

# Quantize
oneshot(
    model="Qwen/Qwen2.5-0.5B",
    dataset=dataset,
    recipe=recipe,
    output_dir="./quantized-model",
    max_seq_length=2048,
    num_calibration_samples=256,
)
```

### Deploy with vLLM
```python
from vllm import LLM, SamplingParams

# Load quantized model
llm = LLM(
    model="./qwen2.5-0.5b-gptq-int4",
    quantization="gptq",
    gpu_memory_utilization=0.4
)

# Generate
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)
prompts = ["The future of AI is"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

## GPU Monitoring

### Check GPU status
```bash
nvidia-smi
```

### Watch GPU in real-time
```bash
watch -n 1 nvidia-smi
```

### Check memory usage
```bash
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv
```

## Model Size Calculation

### FP16 (original)
- Bytes per parameter: 2
- Size (GB) = (num_params × 2) / (1024³)

### INT8 (quantized)
- Bytes per parameter: 1
- Size (GB) = (num_params × 1) / (1024³)
- Compression: ~50%

### INT4 (quantized)
- Bytes per parameter: 0.5
- Size (GB) = (num_params × 0.5) / (1024³)
- Compression: ~75%

## Expected Results (Qwen2.5-0.5B)

| Model | Size | Tokens/sec | Memory |
|-------|------|------------|--------|
| FP16 (original) | ~1.0 GB | Baseline | ~2 GB |
| INT8 (quantized) | ~0.5 GB | ~1.3x | ~1.5 GB |
| INT4 (quantized) | ~0.25 GB | ~1.5-2x | ~1 GB |

*Results may vary based on GPU and batch size*

## Troubleshooting Commands

### Clear GPU memory
```python
import torch
torch.cuda.empty_cache()
```

### Check CUDA availability
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

### Restart Jupyter kernel
Kernel → Restart Kernel (or `00` in command mode)

## Configuration Files

- `configs/gptq_int4.yaml` - INT4 quantization recipe
- `configs/gptq_int8.yaml` - INT8 quantization recipe

## Key Parameters to Experiment With

### Quantization
- `num_bits`: 4, 8 (4 = smaller/faster, 8 = better quality)
- `num_calibration_samples`: 128, 256, 512 (more = better quality, slower)
- `symmetric`: true/false (affects quality/performance)

### vLLM
- `gpu_memory_utilization`: 0.4 - 0.9 (higher = more batch size)
- `max_tokens`: Output length limit
- `temperature`: 0.1 - 1.0 (lower = more deterministic)
