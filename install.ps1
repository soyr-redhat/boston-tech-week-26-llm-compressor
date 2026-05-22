# Boston Tech Week 2026 - LLM Benchmarking Setup (Windows)
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Boston Tech Week 2026" -ForegroundColor Cyan
Write-Host "LLM Benchmarking Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Host "Error: Python 3 is not installed." -ForegroundColor Red
    Write-Host "Please install Python 3.9+ and try again."
    Write-Host "Visit: https://www.python.org/downloads/"
    exit 1
}

$pythonExe = $pythonCmd.Source
Write-Host "Found Python at: $pythonExe"

# Install guidellm
Write-Host "Installing guidellm..." -ForegroundColor Yellow
try {
    & $pythonExe -m pip install --user --upgrade "numpy<2" guidellm 2>&1 | Out-Null
    Write-Host "✓ Installation complete!" -ForegroundColor Green
} catch {
    Write-Host "✗ Installation failed: $_" -ForegroundColor Red
    Write-Host "Try manually: python -m pip install guidellm"
    exit 1
}

# Test installation
Write-Host ""
Write-Host "Testing installation..." -ForegroundColor Yellow
$guidellmCmd = Get-Command guidellm -ErrorAction SilentlyContinue
if ($guidellmCmd) {
    Write-Host "✓ guidellm installed successfully!" -ForegroundColor Green
} else {
    Write-Host "Note: You may need to restart your terminal for guidellm to be available." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Set the model endpoints:"
Write-Host '   $env:ORIGINAL_API="https://vllm-original.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"'
Write-Host '   $env:QUANTIZED_API="https://vllm-quantized.apps.ocp.ntdrq.sandbox503.opentlc.com/v1"'
Write-Host ""
Write-Host "2. Run your first benchmark:"
Write-Host '   guidellm --target "$env:ORIGINAL_API" --model "Qwen/Qwen2.5-7B-Instruct" --data-type emulated --emulated-tokens 100 --request-count 5'
Write-Host ""
Write-Host "For full workshop guide, visit:"
Write-Host "https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor"
Write-Host ""
