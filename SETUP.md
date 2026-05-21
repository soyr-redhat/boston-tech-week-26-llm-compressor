# Workshop Setup Guide

## For Attendees

### Pre-Workshop Checklist

1. **Access your OpenShift account**
   - Username: `userXX` (provided during workshop)
   - Login URL: (provided during workshop)

2. **Launch JupyterHub**
   - Navigate to JupyterHub service in OpenShift
   - Start your notebook server
   - Select environment with GPU access (L40S)

3. **Verify GPU access**
   ```bash
   !nvidia-smi
   ```
   You should see an L40S GPU listed.

4. **Clone workshop materials**
   ```bash
   !git clone https://github.com/soyr-redhat/MIT-build-n-brew-llm-compressor.git
   cd MIT-build-n-brew-llm-compressor
   ```

5. **Setup environment**
   
   Option A: Quick setup with uv (recommended):
   ```bash
   !./setup.sh
   ```
   
   Option B: Manual setup with uv:
   ```bash
   !uv venv
   !source .venv/bin/activate
   !uv pip install -e .
   ```
   
   Option C: Traditional pip (if uv not available):
   ```bash
   !pip install -r requirements.txt
   ```

6. **Open the workshop notebook**
   - Navigate to `workshop_notebook.ipynb`
   - Follow along with the instructor!

---

## For Instructors / Admins

### Pre-Workshop Infrastructure Setup

#### 1. OpenShift Cluster Configuration

Ensure the cluster has:
- 60 user accounts provisioned (`user01` - `user60`)
- GPU node pool with L40S GPUs
- JupyterHub deployed with GPU notebook images
- Sufficient GPU quota per user (at least 1 L40S per user during workshop)

#### 2. Pre-install Dependencies

Option A: Build custom notebook image with uv and all dependencies:
```dockerfile
FROM quay.io/jupyter/pytorch-notebook:latest

USER root
RUN apt-get update && apt-get install -y git curl

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

USER jovyan
WORKDIR /tmp/workshop-setup

# Copy project files
COPY pyproject.toml .
COPY setup.sh .

# Install dependencies with uv
RUN uv venv && \
    /bin/bash -c "source .venv/bin/activate && uv pip install -e ."

# Make uv available globally
ENV PATH="/home/jovyan/.local/bin:${PATH}"
```

Option B: Have users install at workshop start with setup script (~3-5 minutes with uv)

Option C: Traditional pip install (slower, ~5-10 minutes)

#### 3. Pre-cache Models (Recommended)

To avoid 60 simultaneous downloads:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Download to shared cache
model_id = "Qwen/Qwen2.5-0.5B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    cache_dir="/shared/models"  # Shared across users
)
```

Set environment variable for all users:
```bash
export HF_HOME=/shared/models
```

#### 4. Pre-download Calibration Data

Cache C4 dataset to avoid rate limits:
```python
from datasets import load_dataset

dataset = load_dataset(
    "allenai/c4",
    data_files="en/c4-train.00000-of-01024.json.gz",
    split="train",
    cache_dir="/shared/datasets"
)
```

#### 5. Test Setup

Before the workshop:
1. Log in as test user account
2. Run through entire notebook end-to-end
3. Time each section
4. Verify GPU access and memory limits
5. Check network bandwidth for HuggingFace downloads

#### 6. Backup Quantized Models

Pre-quantize models and upload to shared location:
```bash
# After quantizing
tar -czf qwen2.5-0.5b-gptq-int4.tar.gz qwen2.5-0.5b-gptq-int4/
# Upload to shared storage or S3
```

Users can download if quantization fails:
```bash
wget https://<shared-storage>/qwen2.5-0.5b-gptq-int4.tar.gz
tar -xzf qwen2.5-0.5b-gptq-int4.tar.gz
```

#### 7. Helper Scripts

Create a `/shared/scripts/` directory with:
- Quick GPU check script
- Model download script
- Troubleshooting common errors

---

## Troubleshooting

### Common Issues

**"CUDA out of memory"**
- Restart kernel
- Reduce `gpu_memory_utilization` parameter
- Close other notebooks

**"Rate limit exceeded" (HuggingFace)**
- Use pre-cached models (see admin setup)
- Set `HF_TOKEN` environment variable with your token

**Slow quantization**
- Verify GPU is being used: `nvidia-smi`
- Check that CUDA is available: `torch.cuda.is_available()`
- Reduce calibration samples (not recommended for quality)

**vLLM import error**
- Ensure CUDA toolkit is installed
- Check PyTorch CUDA version matches system CUDA

---

## Contact

For issues during the workshop:
- Slack channel: `#build-n-brew-workshop`
- Raise your hand for TA assistance
