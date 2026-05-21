#!/bin/bash
# Setup script for MIT Build & Brew LLM Compressor Workshop

set -e

echo "=========================================="
echo "MIT Build & Brew Workshop Setup"
echo "=========================================="
echo ""

# Detect platform
OS="$(uname -s)"
ARCH="$(uname -m)"

if [[ "$OS" == "Darwin" ]]; then
    echo "⚠️  macOS detected - this workshop requires Linux with CUDA GPUs"
    echo "   Installing minimal dev dependencies for local testing only"
    echo ""
    REQUIREMENTS="requirements-dev.txt"
else
    echo "✓ Linux detected - installing full dependencies"
    echo ""
    REQUIREMENTS="requirements.txt"
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv found: $(which uv)"
echo ""

# Create virtual environment with uv
echo "[1/3] Creating virtual environment with uv..."
uv venv

echo ""
echo "[2/3] Installing dependencies from $REQUIREMENTS..."
uv pip install -r "$REQUIREMENTS"

echo ""
echo "[3/3] Verifying installation..."

# Activate venv and check
source .venv/bin/activate

if [[ "$OS" == "Darwin" ]]; then
    python -c "
import torch
import transformers
print('✓ Core packages imported successfully (dev mode)')
print(f'  PyTorch: {torch.__version__}')
print(f'  Transformers: {transformers.__version__}')
print(f'  CUDA available: {torch.cuda.is_available()}')
print('')
print('⚠️  Note: llmcompressor and vLLM not installed on macOS')
print('   These will be available in the OpenShift GPU environment')
"
else
    python -c "
import torch
import transformers
try:
    import llmcompressor
    import vllm
    llm_ok = True
except ImportError:
    llm_ok = False

print('✓ Core packages imported successfully')
print(f'  PyTorch: {torch.__version__}')
print(f'  Transformers: {transformers.__version__}')
if llm_ok:
    print('  llmcompressor: ✓')
    print('  vLLM: ✓')
print(f'  CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'  GPU: {torch.cuda.get_device_name(0)}')
"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate"
echo ""
if [[ "$OS" == "Darwin" ]]; then
    echo "Note: This is a development setup for macOS"
    echo "Full workshop requires Linux with CUDA GPUs (OpenShift environment)"
    echo ""
fi
echo "To run the workshop notebook:"
echo "  jupyter notebook workshop_notebook.ipynb"
echo ""
echo "To run quantization script:"
echo "  python scripts/quantize_qwen.py --help"
echo ""
