# Boston Tech Week 2026 - LLM Quantization Workshop

**Duration:** 60 minutes  
**Audience:** 50 participants  
**Stack:** vLLM + guidellm + OpenShift

---

## Quick Links

- **Workshop Documentation:** [WORKSHOP_GUIDE.md](WORKSHOP_GUIDE.md)
- **Live Comparison UI:** https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
- **Original API:** `https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1`
- **Quantized API:** `https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1`

---

## Workshop Overview

This hands-on workshop teaches LLM quantization through live demonstration and practical benchmarking.

### Part 1: Theory + Live Demo (30 min)
- Instructor shows side-by-side comparison of FP16 vs INT4 models
- Explains quantization fundamentals and performance benefits
- Real-time metrics displayed in Gradio UI

### Part 2: Hands-On Benchmarking (30 min)
- Participants install `guidellm` on their laptops
- Benchmark both models from their machines
- Compare throughput, latency, and quality

**No cluster access needed for participants!**

---

## For Participants

### Quick Start (2 minutes)

```bash
# 1. Run the installer (Mac/Linux)
curl -sSL https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/install.sh | bash

# Windows: irm https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/install.ps1 | iex

# 2. Set endpoints
export ORIGINAL_API="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"
export QUANTIZED_API="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"

# 3. Benchmark original model
guidellm benchmark \
  --target "$ORIGINAL_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 10

# 4. Benchmark quantized model
guidellm benchmark \
  --target "$QUANTIZED_API" \
  --profile sweep \
  --data "prompt_tokens=100,output_tokens=100" \
  --max-requests 10
```

**Full Guide:** [WORKSHOP_GUIDE.md](WORKSHOP_GUIDE.md) | [Quick Start](QUICK_START.md)

---

## For Instructors

### Pre-Workshop Checklist

```bash
# 1. Verify pods are running
oc get pods -n workshop

# 2. Test comparison UI
open https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com

# 3. Warm up models with test prompts
# (Run 2-3 prompts in the UI)
```

### During Workshop

1. **Demo Phase:** Share screen with [Comparison UI](https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com)
2. **Hands-On:** Guide participants through guidellm installation and benchmarking
3. **Discussion:** Review metrics and discuss production considerations

**Full Walkthrough:** [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md)

---

## Infrastructure

### Architecture

```
┌───────────────────────────────────────┐
│  Participant Laptops (50 users)       │
│  $ pip install guidellm               │
│  $ guidellm --target <endpoint> ...   │
└─────────┬──────────────┬──────────────┘
          │              │
          │ HTTPS        │ HTTPS
          ▼              ▼
    ┌──────────┐   ┌──────────┐
    │ Original │   │Quantized │
    │  FP16    │   │   INT4   │
    │ 2× GPU   │   │ 2× GPU   │
    └──────────┘   └──────────┘
          │              │
    ┌─────┴──────────────┴─────┐
    │  workshop namespace       │
    │  OpenShift Cluster        │
    └───────────────────────────┘
```

### Deployed Services

| Service | Model | GPUs | Endpoint |
|---------|-------|------|----------|
| **Original** | Qwen/Qwen2.5-7B-Instruct (FP16) | 2× L4 | [vllm-original](https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com) |
| **Quantized** | RedHatAI/Qwen3.5-9B-quantized.w4a16 (INT4) | 2× L4 | [vllm-quantized](https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com) |
| **Comparison UI** | Gradio (Everforest theme) | — | [comparison-ui](https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com) |

**Status:** [CLUSTER_STATUS.md](CLUSTER_STATUS.md)

---

## Repository Structure

```
.
├── comparison_ui.py           # Gradio UI for side-by-side comparison
├── openshift/
│   └── workshop-deployment.yaml  # Full deployment manifest
├── docs/                      # GitHub Pages site
│   ├── index.md              # Landing page
│   ├── quick-start.md        # Participant quick ref
│   ├── workshop-guide.md     # Full workshop guide
│   ├── instructor-guide.md   # Instructor walkthrough
│   └── cluster-status.md     # Infrastructure status
├── WORKSHOP_GUIDE.md          # Complete workshop guide
├── QUICK_START.md            # Quick reference card
├── INSTRUCTOR_GUIDE.md       # Instructor walkthrough
└── CLUSTER_STATUS.md         # Cluster ops guide
```

---

## Development

### Local Testing

```bash
# Test comparison UI locally
python comparison_ui.py

# Access at http://localhost:7860
# Update endpoints to point to local vLLM instances if testing
```

### Deploy to OpenShift

```bash
# Create namespace
oc create namespace workshop

# Create UI code ConfigMap
oc create configmap comparison-ui-code \
  --from-file=comparison_ui.py \
  -n workshop

# Deploy all resources
oc apply -f openshift/workshop-deployment.yaml

# Create routes
oc expose service vllm-original \
  --name=vllm-original-api \
  --hostname=vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com \
  -n workshop

oc expose service vllm-quantized \
  --name=vllm-quantized-api \
  --hostname=vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com \
  -n workshop
```

---

## Resources

- **vLLM:** [docs.vllm.ai](https://docs.vllm.ai/)
- **guidellm:** [github.com/neuralmagic/guidellm](https://github.com/neuralmagic/guidellm)
- **LLM Compressor:** [github.com/vllm-project/llm-compressor](https://github.com/vllm-project/llm-compressor)
- **RedHat AI Models:** [huggingface.co/RedHatAI](https://huggingface.co/RedHatAI)

---

## License

MIT - Feel free to use this workshop content for your own events!

---

## Questions?

- During workshop: Raise your hand
- After workshop: Boston Tech Week Slack
