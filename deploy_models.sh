#!/bin/bash
# Deploy vLLM models for comparison workshop

set -e

echo "============================================"
echo "Boston Tech Week 2026 - vLLM Deployment"
echo "============================================"
echo ""

# Default models
ORIGINAL_MODEL="${ORIGINAL_MODEL:-Qwen/Qwen2.5-0.5B}"
QUANTIZED_MODEL="${QUANTIZED_MODEL:-neuralmagic/Qwen2.5-0.5B-Instruct-FP8}"

echo "Models to deploy:"
echo "  Original:  $ORIGINAL_MODEL (port 8080)"
echo "  Quantized: $QUANTIZED_MODEL (port 8081)"
echo ""

# Check GPU
if ! nvidia-smi &>/dev/null; then
    echo "⚠️  Warning: No GPU detected. vLLM requires a GPU."
    echo "   Continuing anyway for testing..."
fi

# Deploy original model
echo "[1/2] Starting original model on port 8080..."
vllm serve "$ORIGINAL_MODEL" \
    --port 8080 \
    --host 0.0.0.0 \
    > vllm_original.log 2>&1 &

ORIG_PID=$!
echo "  Started with PID $ORIG_PID"

# Wait a bit
sleep 3

# Deploy quantized model
echo "[2/2] Starting quantized model on port 8081..."
vllm serve "$QUANTIZED_MODEL" \
    --port 8081 \
    --host 0.0.0.0 \
    --quantization fp8 \
    > vllm_quantized.log 2>&1 &

QUANT_PID=$!
echo "  Started with PID $QUANT_PID"

echo ""
echo "============================================"
echo "Deployment Complete!"
echo "============================================"
echo ""
echo "vLLM servers starting (may take 30-60 seconds to load models)..."
echo ""
echo "Logs:"
echo "  Original:  tail -f vllm_original.log"
echo "  Quantized: tail -f vllm_quantized.log"
echo ""
echo "Test endpoints:"
echo "  curl http://localhost:8080/health"
echo "  curl http://localhost:8081/health"
echo ""
echo "Once models are loaded, run:"
echo "  python comparison_ui.py"
echo ""
echo "To stop servers:"
echo "  kill $ORIG_PID $QUANT_PID"
echo ""
