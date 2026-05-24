# Local Setup Guide

If you can't access the OpenShift workshop environment, you can run the workshop notebook locally on your machine.

---

## Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **Internet connection** (to access vLLM model endpoints)
- **~500MB disk space** for dependencies

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor.git
cd boston-tech-week-26-llm-compressor
```

### 2. Run the Setup Script

```bash
./scripts/build_local.sh
```

The script will:
- Detect your OS (macOS, Linux, or WSL)
- Check Python version
- Create a virtual environment
- Install JupyterLab, guidellm, and other dependencies
- Verify vLLM endpoints are accessible
- Open the workshop notebook in your browser

### 3. Follow the Notebook

Once JupyterLab opens:
1. Navigate to `notebooks/workshop_notebook.ipynb`
2. Run each cell in order (Shift+Enter)
3. Follow the instructions in the notebook

---

## Manual Setup

If the automated script doesn't work, follow these manual steps:

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv-workshop

# Activate it
# On macOS/Linux:
source .venv-workshop/bin/activate
# On Windows:
.venv-workshop\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install jupyterlab guidellm matplotlib pandas ipywidgets
```

### 3. Start JupyterLab

```bash
jupyter lab --notebook-dir=.
```

### 4. Open the Notebook

In JupyterLab, navigate to:
```
notebooks/workshop_notebook.ipynb
```

---

## Supported Operating Systems

| OS | Support | Notes |
|----|---------|-------|
| **macOS** | Full | Recommended: Install Python via Homebrew |
| **Linux** | Full | Tested on Ubuntu 22.04+, Fedora 38+ |
| **Windows (WSL)** | Full | Use WSL2 with Ubuntu |
| **Windows (native)** | Partial | Use PowerShell, may need manual setup |

---

## Troubleshooting

### Python Not Found

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

**WSL:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

### Virtual Environment Creation Fails

If `python3 -m venv` fails, you may need to install `python3-venv`:

```bash
# Ubuntu/Debian/WSL
sudo apt-get install python3-venv

# Fedora/RHEL
sudo dnf install python3-virtualenv
```

### JupyterLab Won't Open

If the script can't auto-open your browser:

1. Look for output like:
   ```
   http://127.0.0.1:8888/lab?token=abc123...
   ```
2. Copy and paste that URL into your browser manually

### Cannot Connect to vLLM Endpoints

The benchmarking requires access to the hosted vLLM models. If you see connection errors:

1. **Check internet connection** - You need access to the OpenShift cluster
2. **Check VPN** - Some corporate networks may block external endpoints
3. **Use workshop Wi-Fi** - If at the event, connect to the provided network

The endpoints are:
- Original (FP16): `https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1`
- Quantized (INT4): `https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1`

You can test connectivity with:
```bash
curl https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models
```

### Package Installation Fails

If `pip install` fails:

1. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```

2. **Install packages one at a time:**
   ```bash
   pip install jupyterlab
   pip install guidellm
   pip install matplotlib pandas
   ```

3. **Check disk space:**
   ```bash
   df -h
   ```

---

## What Gets Installed

The local setup installs these packages:

| Package | Purpose | Size |
|---------|---------|------|
| **JupyterLab** | Interactive notebook environment | ~150MB |
| **guidellm** | LLM benchmarking tool | ~50MB |
| **matplotlib** | Visualization library | ~30MB |
| **pandas** | Data analysis | ~20MB |
| **ipywidgets** | Interactive notebook widgets | ~10MB |

Total: **~260MB** (plus Python dependencies)

---

## Cleanup

When you're done with the workshop:

### Deactivate Virtual Environment

```bash
deactivate
```

### Remove Virtual Environment

```bash
rm -rf .venv-workshop
```

### Keep the Repo for Later

The repository and notebook are useful references! Consider keeping them to:
- Review the quantization concepts
- Try benchmarking other models
- Share with colleagues

---

## Next Steps

After completing the local workshop:

1. **Try quantizing your own model** with [LLM Compressor](https://github.com/vllm-project/llm-compressor)
2. **Deploy vLLM locally** with [Docker](https://docs.vllm.ai/en/latest/getting_started/installation.html)
3. **Explore RedHat AI models** at [huggingface.co/RedHatAI](https://huggingface.co/RedHatAI)

---

## Questions?

- **During workshop:** Ask the instructor
- **After workshop:** Open an issue on [GitHub](https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor/issues)
