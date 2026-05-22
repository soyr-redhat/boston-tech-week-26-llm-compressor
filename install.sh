#!/bin/bash
set -e

# Boston Tech Week 2026 - LLM Benchmarking Setup
# This script installs guidellm for the workshop

echo "========================================="
echo "Boston Tech Week 2026"
echo "LLM Benchmarking Setup"
echo "========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.9+ and try again."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Detect if pipx is available (best option)
if command -v pipx &> /dev/null; then
    echo "Using pipx for installation (best isolation)..."
    pipx install guidellm --force 2>/dev/null || pipx install guidellm
    INSTALL_METHOD="pipx"
# Check if uv is available
elif command -v uv &> /dev/null; then
    echo "Using uv for installation..."
    uv tool install guidellm --force 2>/dev/null || uv tool install guidellm
    INSTALL_METHOD="uv"
# Fall back to pip with user install
else
    echo "Installing guidellm with pip..."
    # Use --user to avoid permission issues
    python3 -m pip install --user --upgrade 'numpy<2' guidellm 2>&1 | grep -v "WARNING: Ignoring invalid distribution" || true
    INSTALL_METHOD="pip"

    # Add user bin to PATH if not already there
    USER_BIN="$HOME/.local/bin"
    if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
        echo ""
        echo "Note: Adding $USER_BIN to PATH for this session"
        export PATH="$USER_BIN:$PATH"

        # Suggest adding to shell profile
        SHELL_NAME=$(basename "$SHELL")
        if [ "$SHELL_NAME" = "zsh" ]; then
            PROFILE="$HOME/.zshrc"
        elif [ "$SHELL_NAME" = "bash" ]; then
            PROFILE="$HOME/.bashrc"
        fi

        if [ -n "$PROFILE" ]; then
            echo "To make this permanent, add this to your $PROFILE:"
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        fi
    fi
fi

echo ""
echo "Testing installation..."

# Test if guidellm is available
if command -v guidellm &> /dev/null; then
    echo "✓ guidellm installed successfully!"
    echo ""
    echo "Installation method: $INSTALL_METHOD"
    guidellm --version 2>/dev/null || echo "(version check skipped)"
else
    echo "✗ Installation failed. Please try manual installation:"
    echo "  pip install guidellm"
    exit 1
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Set the model endpoints:"
echo "   export ORIGINAL_API=\"https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1\""
echo "   export QUANTIZED_API=\"https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1\""
echo ""
echo "2. Run your first benchmark:"
echo "   guidellm benchmark --target \"\$ORIGINAL_API\" --profile sweep --data \"prompt_tokens=100,output_tokens=100\" --max-requests 5"
echo ""
echo "For full workshop guide, visit:"
echo "https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor"
echo ""
