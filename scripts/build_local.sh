#!/usr/bin/env bash
#
# Local Workshop Setup Script
# Fallback for running the workshop notebook locally if OpenShift provisioning fails
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$REPO_ROOT/.venv-workshop"
NOTEBOOK_PATH="$REPO_ROOT/notebooks/workshop_notebook.ipynb"

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Boston Tech Week 2026 - Local Workshop Setup             ║${NC}"
echo -e "${GREEN}║  LLM Quantization Workshop - Local Fallback               ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
detect_os() {
    echo -e "${YELLOW}→${NC} Detecting operating system..."

    case "$(uname -s)" in
        Darwin*)
            OS="macOS"
            OPEN_CMD="open"
            ;;
        Linux*)
            OS="Linux"
            OPEN_CMD="xdg-open"
            # Check if running in WSL
            if grep -qi microsoft /proc/version 2>/dev/null; then
                OS="WSL"
                OPEN_CMD="explorer.exe"
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            OS="Windows"
            OPEN_CMD="start"
            ;;
        *)
            echo -e "${RED}✗${NC} Unsupported OS: $(uname -s)"
            echo "  This script supports macOS, Linux, and WSL."
            exit 1
            ;;
    esac

    echo -e "${GREEN}✓${NC} Detected: $OS"
}

# Check Python version
check_python() {
    echo -e "${YELLOW}→${NC} Checking Python installation..."

    # Try python3 first, then python
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}✗${NC} Python not found"
        echo ""
        echo "  Please install Python 3.8 or higher:"
        echo "    macOS:  brew install python3"
        echo "    Linux:  sudo apt-get install python3 python3-venv"
        echo "    WSL:    sudo apt-get install python3 python3-venv"
        exit 1
    fi

    # Check version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]; }; then
        echo -e "${RED}✗${NC} Python $PYTHON_VERSION detected (need 3.8+)"
        echo "  Please upgrade to Python 3.8 or higher"
        exit 1
    fi

    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION ($PYTHON_CMD)"
}

# Create virtual environment
create_venv() {
    echo -e "${YELLOW}→${NC} Setting up virtual environment..."

    if [ -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}!${NC} Virtual environment already exists at $VENV_DIR"
        read -p "  Remove and recreate? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
        else
            echo -e "${GREEN}✓${NC} Using existing virtual environment"
            return
        fi
    fi

    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "${GREEN}✓${NC} Virtual environment created: $VENV_DIR"
}

# Activate virtual environment
activate_venv() {
    echo -e "${YELLOW}→${NC} Activating virtual environment..."

    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        echo -e "${GREEN}✓${NC} Virtual environment activated"
    else
        echo -e "${RED}✗${NC} Could not find activation script"
        exit 1
    fi
}

# Install requirements
install_requirements() {
    echo -e "${YELLOW}→${NC} Installing Python packages..."
    echo "  This may take 2-3 minutes..."
    echo ""

    # Upgrade pip first
    pip install --quiet --upgrade pip

    # Install workshop dependencies
    pip install --quiet \
        jupyterlab \
        guidellm \
        matplotlib \
        pandas \
        ipywidgets

    echo ""
    echo -e "${GREEN}✓${NC} Packages installed:"
    echo "    • JupyterLab (notebook environment)"
    echo "    • guidellm (LLM benchmarking)"
    echo "    • matplotlib (visualization)"
    echo "    • pandas (data analysis)"
}

# Check vLLM endpoints
check_endpoints() {
    echo -e "${YELLOW}→${NC} Checking vLLM model endpoints..."

    ORIGINAL_ENDPOINT="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models"
    QUANTIZED_ENDPOINT="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1/models"

    # Check original
    if curl -s --max-time 5 "$ORIGINAL_ENDPOINT" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Original model (FP16) is accessible"
    else
        echo -e "${YELLOW}!${NC} Original model endpoint not responding"
        echo "  This is okay - you can still view the notebook"
    fi

    # Check quantized
    if curl -s --max-time 5 "$QUANTIZED_ENDPOINT" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Quantized model (INT4) is accessible"
    else
        echo -e "${YELLOW}!${NC} Quantized model endpoint not responding"
        echo "  This is okay - you can still view the notebook"
    fi
}

# Start Jupyter
start_jupyter() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  Starting JupyterLab...                                   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}→${NC} JupyterLab will open in your browser"
    echo -e "${YELLOW}→${NC} Navigate to: notebooks/workshop_notebook.ipynb"
    echo ""
    echo -e "${YELLOW}To stop JupyterLab:${NC} Press Ctrl+C in this terminal"
    echo ""

    # Wait a moment before opening
    sleep 2

    # Start Jupyter in the background to get the URL first
    jupyter lab --notebook-dir="$REPO_ROOT" --no-browser --port=8888 > /tmp/jupyter_output.log 2>&1 &
    JUPYTER_PID=$!

    # Wait for Jupyter to start and capture the token URL
    echo -e "${YELLOW}→${NC} Waiting for JupyterLab to start..."
    sleep 3

    # Get the URL with token
    JUPYTER_URL=$(grep -o 'http://127.0.0.1:8888/lab?token=[a-zA-Z0-9]*' /tmp/jupyter_output.log | head -1)

    if [ -z "$JUPYTER_URL" ]; then
        # Fallback to launching without capturing URL
        echo -e "${YELLOW}!${NC} Could not capture token URL, opening default..."
        $OPEN_CMD "http://localhost:8888/lab/tree/notebooks/workshop_notebook.ipynb" 2>/dev/null
    else
        # Open the notebook directly with token
        NOTEBOOK_URL="${JUPYTER_URL/\/lab?/\/lab\/tree\/notebooks\/workshop_notebook.ipynb?}"
        echo -e "${GREEN}✓${NC} Opening notebook in browser..."
        $OPEN_CMD "$NOTEBOOK_URL" 2>/dev/null
    fi

    # Bring Jupyter to foreground
    wait $JUPYTER_PID
}

# Main execution
main() {
    detect_os
    check_python
    create_venv
    activate_venv
    install_requirements
    check_endpoints
    start_jupyter
}

# Run main
main
