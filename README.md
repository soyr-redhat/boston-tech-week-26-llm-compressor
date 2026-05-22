# Boston Tech Week 2026 - LLM Quantization Workshop

**Duration:** 60 minutes  
**Audience:** 50 participants  
**Stack:** vLLM + guidellm + JupyterLab + OpenShift

---

## Quick Links

- **Workshop Landing Page:** https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com
- **Documentation:** https://soyr-redhat.github.io/boston-tech-week-26-llm-compressor/
- **Comparison UI (Instructor Demo):** https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com

---

## Workshop Overview

This hands-on workshop teaches LLM quantization through live demonstration and practical benchmarking.

### Part 1: Theory + Live Demo (30 min)
- Instructor shows side-by-side comparison of FP16 vs INT4 models
- Explains quantization fundamentals and performance benefits
- Real-time metrics displayed in Gradio UI

### Part 2: Hands-On Benchmarking (30 min)
- Participants use pre-provisioned JupyterLab instances in their browser
- Benchmark both models using guidellm
- Compare throughput, latency, and resource usage

**No installation required for participants!**

---

## For Participants

### Getting Your Workspace

1. Visit the workshop landing page: **https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com**
2. Click "Get My Workspace" to receive your unique JupyterLab URL
3. Bookmark your workspace URL (you'll be auto-redirected)
4. Open `workshop_notebook.ipynb` and follow along

Your workspace includes:
- Pre-configured JupyterLab environment
- Workshop notebook with all instructions
- guidellm pre-installed for benchmarking
- Isolated from other participants (NetworkPolicy enforced)
- Works on any device with a web browser

**Full Documentation:** https://soyr-redhat.github.io/boston-tech-week-26-llm-compressor/

---

## For Instructors

### Pre-Workshop Setup

1. **Provision User Workspaces:**
   ```bash
   SECRET_KEY="boston-tech-week-2026-secret" ./scripts/provision-users.sh 50
   ```

2. **Verify Infrastructure:**
   ```bash
   # Check all pods are running
   oc get pods -n workshop
   
   # Test comparison UI
   open https://comparison-ui.apps.ocp.ntdrq.sandbox503.opentlc.com
   
   # Test assignment app
   open https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com
   ```

3. **Reset Assignment Counter (if needed):**
   ```bash
   curl https://workshop.apps.ocp.ntdrq.sandbox503.opentlc.com/reset
   ```

### During Workshop

1. **Opening (5 min):** Share workshop landing page URL with participants
2. **Demo Phase (25 min):** Live comparison using Gradio UI
3. **Hands-On (30 min):** Guide participants through Jupyter notebook
4. **Discussion:** Review metrics and production considerations

**Pre-Event Checklist:** [pre-event-checklist.md](docs/pre-event-checklist.md)

---

## Architecture

### Infrastructure Layout

```
┌─────────────────────────────────────────────┐
│  Participants (50 users)                    │
│  Browser → JupyterLab (user-specific URL)   │
│  Runs guidellm from notebook                │
└────────────┬────────────────────────────────┘
             │
             │ HTTPS (Public Routes)
             ▼
   ┌──────────────────────────────┐
   │  Shared vLLM Services        │
   │  ┌──────────┐  ┌──────────┐ │
   │  │ Original │  │Quantized │ │
   │  │  FP16    │  │   INT4   │ │
   │  │ 2x GPU   │  │ 2x GPU   │ │
   │  └──────────┘  └──────────┘ │
   └──────────────────────────────┘
             │
   ┌─────────┴─────────────────────┐
   │  workshop namespace           │
   │  - 50 JupyterLab instances    │
   │  - Assignment app             │
   │  - Comparison UI              │
   │  - NetworkPolicy (isolation)  │
   └───────────────────────────────┘
```

### Deployed Services

| Service | Model | GPUs | Purpose |
|---------|-------|------|---------|
| **vLLM Original** | Qwen/Qwen2.5-7B-Instruct (FP16) | 2x L4 | Baseline model |
| **vLLM Quantized** | RedHatAI/Qwen3.5-9B-quantized.w4a16 (INT4) | 2x L4 | Quantized comparison |
| **Assignment App** | Flask | - | Auto-assigns users to workspaces |
| **Comparison UI** | Gradio | - | Instructor demo interface |
| **JupyterLab (50x)** | scipy-notebook | - | Per-user workshop environments |

**Security:** [docs/SECURITY.md](docs/SECURITY.md)

---

## Repository Structure

```
.
├── apps/
│   ├── assignment_app.py          # Auto-assignment Flask app
│   └── comparison_ui.py           # Gradio side-by-side demo UI
├── notebooks/
│   └── workshop_notebook.ipynb    # Workshop Jupyter notebook
├── openshift/
│   ├── workshop-deployment.yaml   # vLLM + comparison UI
│   ├── jupyter-user-template.yaml # Per-user JupyterLab template
│   └── jupyter-network-policy.yaml # User isolation
├── scripts/
│   ├── provision-users.sh         # Provision N JupyterLab instances
│   ├── deploy-assignment.sh       # Deploy assignment app
│   ├── cleanup-users.sh           # Clean up user workspaces
│   ├── install.sh                 # Install script (Mac/Linux)
│   └── install.ps1                # Install script (Windows)
├── docs/                          # GitHub Pages documentation
│   ├── index.md
│   ├── quick-start.md
│   ├── workshop-guide.md
│   ├── instructor-guide.md
│   ├── cluster-status.md
│   ├── pre-event-checklist.md     # Pre-workshop setup checklist
│   └── SECURITY.md                # Security architecture
├── README.md                      # This file
├── pyproject.toml                 # Project metadata
└── mkdocs.yml                     # Documentation config
```

---

## Key Features

### Auto-Assignment System
- Users visit landing page and get auto-assigned to a workspace
- Deterministic URL suffixes prevent cross-user access
- Session persistence (users can return to same workspace)
- Auto-provisioning for overflow capacity

### Security Through Obscurity
- URLs include hash-based suffix (e.g., `jupyter-user1-a0c3761d23`)
- NetworkPolicy blocks pod-to-pod access between users
- No authentication required (minimal friction for 60-min workshop)
- See [docs/SECURITY.md](docs/SECURITY.md) for details

### Zero Installation
- Everything runs in browser via JupyterLab
- guidellm, matplotlib, pandas pre-installed
- No Python, pip, or local environment needed
- Works on Windows, Mac, Linux, ChromeOS

---

## Models

### Original Model
- **Name:** Qwen/Qwen2.5-7B-Instruct
- **Precision:** FP16
- **Size:** ~14GB
- **GPUs:** 2x NVIDIA L4
- **Endpoint:** https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1

### Quantized Model
- **Name:** RedHatAI/Qwen3.5-9B-quantized.w4a16
- **Precision:** INT4 (weights), INT16 (activations)
- **Size:** ~5GB
- **GPUs:** 2x NVIDIA L4
- **Endpoint:** https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1

**Performance Expectations:**
- 1.5-2x throughput improvement
- 30-40% latency reduction
- 50-75% memory savings
- <2% quality degradation

---

## Resources

- **vLLM:** [docs.vllm.ai](https://docs.vllm.ai/)
- **guidellm:** [github.com/vllm-project/guidellm](https://github.com/vllm-project/guidellm)
- **LLM Compressor:** [github.com/vllm-project/llm-compressor](https://github.com/vllm-project/llm-compressor)
- **RedHat AI Models:** [huggingface.co/RedHatAI](https://huggingface.co/RedHatAI)
- **OpenShift:** [docs.openshift.com](https://docs.openshift.com/)

---

## License

MIT - Feel free to use this workshop content for your own events!

---

## Questions?

- During workshop: Ask the instructor
- After workshop: Open an issue on GitHub
