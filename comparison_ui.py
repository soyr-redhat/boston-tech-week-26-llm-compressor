#!/usr/bin/env python3
"""
Side-by-Side vLLM Model Comparison UI
Boston Tech Week 2026 - LLM Quantization Workshop
"""

import gradio as gr
import requests
import time
import json
import threading
from typing import Dict, Tuple

def query_vllm_stream(port: str, prompt: str, max_tokens: int = 100):
    """Query a vLLM endpoint with streaming and yield chunks"""
    # Support both localhost:port and service:port formats
    if ':' in port:
        base_url = f"http://{port}"
    else:
        base_url = f"http://localhost:{port}"

    # Get the actual model name from /v1/models endpoint
    try:
        models_response = requests.get(f"{base_url}/v1/models", timeout=5)
        if models_response.status_code == 200:
            model_name = models_response.json()['data'][0]['id']
        else:
            model_name = "deployed-model"  # fallback
    except:
        model_name = "deployed-model"  # fallback

    payload = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": True
    }

    url = f"{base_url}/v1/completions"

    try:
        start_time = time.time()
        response = requests.post(url, json=payload, stream=True, timeout=60)

        if response.status_code != 200:
            yield f"Error {response.status_code}: {response.text}", {}
            return

        full_text = ""
        token_count = 0

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('text', '')
                            if delta:
                                full_text += delta
                                token_count += 1
                                yield full_text, None
                    except:
                        pass

        elapsed = time.time() - start_time
        metrics = {
            "latency_ms": round(elapsed * 1000, 2),
            "tokens": token_count,
            "tokens_per_sec": round(token_count / elapsed, 2) if elapsed > 0 else 0,
            "total_time": round(elapsed, 2)
        }

        yield full_text, metrics

    except requests.exceptions.ConnectionError:
        endpoint = port if ':' in port else f"localhost:{port}"
        yield f"❌ Cannot connect to {endpoint}. Is vLLM running?", {}
    except Exception as e:
        yield f"❌ Error: {str(e)}", {}

def compare_models(prompt: str, original_port: str, quantized_port: str, max_tokens: int):
    """Compare responses from both models with concurrent streaming"""

    if not prompt.strip():
        yield "⚠️ Please enter a prompt", "", ""
        return

    # Shared state between threads
    state = {
        'orig_text': '',
        'orig_metrics': None,
        'quant_text': '',
        'quant_metrics': None,
        'orig_done': False,
        'quant_done': False,
    }

    def stream_original():
        for text, metrics in query_vllm_stream(original_port, prompt, max_tokens):
            state['orig_text'] = text
            if metrics:
                state['orig_metrics'] = metrics
                state['orig_done'] = True

    def stream_quantized():
        for text, metrics in query_vllm_stream(quantized_port, prompt, max_tokens):
            state['quant_text'] = text
            if metrics:
                state['quant_metrics'] = metrics
                state['quant_done'] = True

    # Start both models in parallel
    orig_thread = threading.Thread(target=stream_original)
    quant_thread = threading.Thread(target=stream_quantized)

    orig_thread.start()
    quant_thread.start()

    # Stream updates while both are running
    while not (state['orig_done'] and state['quant_done']):
        # Format original output
        orig_result = f"**Response:**\n{state['orig_text']}\n\n"
        if state['orig_metrics']:
            orig_result += f"**Metrics:**\n"
            orig_result += f"⏱️ Latency: {state['orig_metrics']['latency_ms']}ms\n"
            orig_result += f"🚀 Speed: {state['orig_metrics']['tokens_per_sec']} tokens/sec\n"
            orig_result += f"📊 Tokens: {state['orig_metrics']['tokens']}"
        elif state['orig_text']:
            orig_result += f"*Generating...*"
        else:
            orig_result = "*Waiting for response...*"

        # Format quantized output
        quant_result = f"**Response:**\n{state['quant_text']}\n\n"
        if state['quant_metrics']:
            quant_result += f"**Metrics:**\n"
            quant_result += f"⏱️ Latency: {state['quant_metrics']['latency_ms']}ms\n"
            quant_result += f"🚀 Speed: {state['quant_metrics']['tokens_per_sec']} tokens/sec\n"
            quant_result += f"📊 Tokens: {state['quant_metrics']['tokens']}"
        elif state['quant_text']:
            quant_result += f"*Generating...*"
        else:
            quant_result = "*Waiting for response...*"

        yield orig_result, quant_result, ""
        time.sleep(0.1)  # Update every 100ms

    # Wait for threads to complete
    orig_thread.join()
    quant_thread.join()

    # Final outputs with metrics
    orig_result = f"**Response:**\n{state['orig_text']}\n\n"
    if state['orig_metrics']:
        orig_result += f"**Metrics:**\n"
        orig_result += f"⏱️ Latency: {state['orig_metrics']['latency_ms']}ms\n"
        orig_result += f"🚀 Speed: {state['orig_metrics']['tokens_per_sec']} tokens/sec\n"
        orig_result += f"📊 Tokens: {state['orig_metrics']['tokens']}"

    quant_result = f"**Response:**\n{state['quant_text']}\n\n"
    if state['quant_metrics']:
        quant_result += f"**Metrics:**\n"
        quant_result += f"⏱️ Latency: {state['quant_metrics']['latency_ms']}ms\n"
        quant_result += f"🚀 Speed: {state['quant_metrics']['tokens_per_sec']} tokens/sec\n"
        quant_result += f"📊 Tokens: {state['quant_metrics']['tokens']}"

    # Final comparison summary
    if state['orig_metrics'] and state['quant_metrics']:
        speedup = state['quant_metrics']['tokens_per_sec'] / state['orig_metrics']['tokens_per_sec']
        latency_reduction = ((state['orig_metrics']['latency_ms'] - state['quant_metrics']['latency_ms']) / state['orig_metrics']['latency_ms']) * 100

        summary = f"""
## 📊 Comparison Results

**Speedup:** {speedup:.2f}x faster
**Latency Improvement:** {abs(latency_reduction):.1f}% {'faster' if latency_reduction > 0 else 'slower'}

| Metric | Original (FP16) | Quantized (INT4) | Difference |
|--------|----------------|------------------|------------|
| Latency | {state['orig_metrics']['latency_ms']}ms | {state['quant_metrics']['latency_ms']}ms | {abs(latency_reduction):.1f}% |
| Speed | {state['orig_metrics']['tokens_per_sec']} tok/s | {state['quant_metrics']['tokens_per_sec']} tok/s | {speedup:.2f}x |
| Tokens | {state['orig_metrics']['tokens']} | {state['quant_metrics']['tokens']} | Same |

**Quality Check:** Compare the text responses above to assess if quantization affected output quality.
"""
    else:
        summary = "⚠️ Could not generate comparison (one or both models failed to respond)"

    yield orig_result, quant_result, summary

# Gradio UI
with gr.Blocks(title="vLLM Model Comparison", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚀 Boston Tech Week 2026: vLLM Model Comparison

    ## Compare Original vs Quantized Model Performance

    This tool lets you compare the speed and quality of:
    - **Original Model** (FP16): Full precision, slower, more memory
    - **Quantized Model** (INT4/INT8): Compressed, faster, less memory
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ⚙️ vLLM Server Configuration")
            original_port = gr.Textbox(
                label="Original Model Endpoint",
                value="vllm-original:8080",
                placeholder="8080 or vllm-original:8080"
            )
            quantized_port = gr.Textbox(
                label="Quantized Model Endpoint",
                value="vllm-quantized:8081",
                placeholder="8081 or vllm-quantized:8081"
            )
            max_tokens = gr.Slider(
                minimum=50,
                maximum=500,
                value=100,
                step=10,
                label="Max Tokens to Generate",
            )

    gr.Markdown("### 💬 Enter Your Prompt")
    prompt = gr.Textbox(
        label="Prompt",
        placeholder="The future of artificial intelligence is...",
        lines=3
    )

    compare_btn = gr.Button("🔍 Compare Models", variant="primary", size="lg")

    gr.Markdown("---")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📝 Original Model (FP16)")
            original_output = gr.Markdown()

        with gr.Column():
            gr.Markdown("### ⚡ Quantized Model (INT4/INT8)")
            quantized_output = gr.Markdown()

    gr.Markdown("---")

    comparison_summary = gr.Markdown()

    # Example prompts
    gr.Examples(
        examples=[
            ["The future of artificial intelligence is", "vllm-original:8080", "vllm-quantized:8081", 100],
            ["Write a Python function to sort a list", "vllm-original:8080", "vllm-quantized:8081", 150],
            ["Explain quantum computing in simple terms:", "vllm-original:8080", "vllm-quantized:8081", 200],
            ["What are the key benefits of model compression?", "vllm-original:8080", "vllm-quantized:8081", 100],
            ["Tell me a short story about a robot", "vllm-original:8080", "vllm-quantized:8081", 200],
        ],
        inputs=[prompt, original_port, quantized_port, max_tokens],
    )

    compare_btn.click(
        fn=compare_models,
        inputs=[prompt, original_port, quantized_port, max_tokens],
        outputs=[original_output, quantized_output, comparison_summary]
    )

    gr.Markdown("""
    ---
    ### 📚 How to Use

    1. **Start vLLM servers** for both models (see workshop instructions)
    2. **Enter the ports** where your vLLM servers are running (default: 8080 and 8081)
    3. **Type a prompt** or select an example
    4. **Click "Compare Models"** to see side-by-side results
    5. **Analyze** the speed difference and quality trade-offs

    ### 🎯 What to Look For

    - **Speed Gains:** Quantized models typically run 1.3-2x faster
    - **Latency:** 30-50% reduction in response time
    - **Quality:** Minimal degradation in output quality
    - **Memory:** ~70-75% reduction in VRAM usage (check `nvidia-smi`)
    """)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
