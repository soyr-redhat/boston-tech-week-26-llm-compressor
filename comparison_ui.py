#!/usr/bin/env python3
"""
vLLM Model Comparison - Everforest Theme
Boston Tech Week 2026 - LLM Quantization Workshop
"""

import gradio as gr
import requests
import time
import json
import threading
from typing import Dict, Tuple

# Everforest-inspired CSS matching nvim config
EVERFOREST_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
    /* Everforest Medium Dark palette */
    --bg0: #2f383e;
    --bg1: #374247;
    --bg2: #404c51;
    --bg3: #4a555b;
    --bg4: #525c62;
    --bg-red: #4c3743;
    --bg-visual: #503946;
    --bg-yellow: #4d4c43;
    --bg-green: #3c4841;
    --bg-blue: #384b55;

    --fg: #d3c6aa;
    --red: #e67e80;
    --orange: #e69875;
    --yellow: #dbbc7f;
    --green: #a7c080;
    --aqua: #83c092;
    --blue: #7fbbb3;
    --purple: #d699b6;
    --grey0: #7a8478;
    --grey1: #859289;
    --grey2: #9da9a0;

    --statusline1: #a7c080;
    --statusline2: #d3c6aa;
    --statusline3: #e67e80;
}

* {
    box-sizing: border-box;
}

body, .gradio-container {
    background: var(--bg0) !important;
    font-family: 'IBM Plex Sans', system-ui, -apple-system, sans-serif !important;
    color: var(--fg) !important;
    line-height: 1.6;
}

/* Main container */
#component-0, .contain, .wrap {
    background: var(--bg0) !important;
    border: 1px solid var(--bg3) !important;
    border-radius: 6px !important;
    padding: 24px !important;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: var(--green) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    margin-bottom: 12px !important;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 1.75rem !important;
    color: var(--statusline1) !important;
    border-bottom: 1px solid var(--bg3);
    padding-bottom: 12px;
    margin-bottom: 24px !important;
}

h2 {
    font-size: 1.25rem !important;
    color: var(--aqua) !important;
}

h3 {
    font-size: 1.1rem !important;
    color: var(--blue) !important;
}

/* Text and paragraphs */
p, span, label, .prose {
    color: var(--fg) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

/* Code and monospace */
code, pre, .input-text {
    font-family: 'IBM Plex Mono', 'Courier New', monospace !important;
    background: var(--bg1) !important;
    color: var(--fg) !important;
}

pre {
    border: 1px solid var(--bg3) !important;
    border-radius: 4px !important;
    padding: 12px !important;
}

code {
    padding: 2px 6px !important;
    border-radius: 3px !important;
}

/* Input fields */
input[type="text"], textarea, .input-text {
    background: var(--bg1) !important;
    border: 1px solid var(--bg3) !important;
    border-radius: 4px !important;
    color: var(--fg) !important;
    padding: 8px 12px !important;
    transition: all 0.2s ease;
}

input:focus, textarea:focus {
    border-color: var(--green) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(167, 192, 128, 0.15) !important;
}

input::placeholder, textarea::placeholder {
    color: var(--grey1) !important;
}

/* Buttons */
button {
    background: var(--bg-green) !important;
    border: 1px solid var(--green) !important;
    color: var(--green) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease;
    cursor: pointer;
}

button:hover {
    background: var(--green) !important;
    color: var(--bg0) !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(167, 192, 128, 0.2);
}

button:active {
    transform: translateY(0);
}

/* Primary button variant */
.primary {
    background: var(--green) !important;
    color: var(--bg0) !important;
    border-color: var(--green) !important;
}

.primary:hover {
    background: var(--aqua) !important;
    border-color: var(--aqua) !important;
}

/* Output areas */
.markdown-output, .output-markdown, .prose {
    background: var(--bg1) !important;
    border: 1px solid var(--bg3) !important;
    border-radius: 4px !important;
    padding: 16px !important;
    color: var(--fg) !important;
    min-height: 200px;
}

/* Slider */
input[type="range"] {
    accent-color: var(--green);
}

.slider-container {
    background: var(--bg1) !important;
    border-radius: 4px !important;
    padding: 12px !important;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
}

th, td {
    border: 1px solid var(--bg3) !important;
    padding: 10px !important;
    text-align: left;
    color: var(--fg) !important;
}

th {
    background: var(--bg2) !important;
    color: var(--green) !important;
    font-weight: 600;
}

tr:nth-child(even) {
    background: var(--bg1) !important;
}

/* Status indicators */
strong {
    color: var(--yellow) !important;
    font-weight: 600;
}

/* Links */
a {
    color: var(--blue) !important;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}

a:hover {
    border-bottom-color: var(--blue);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: var(--bg1);
}

::-webkit-scrollbar-thumb {
    background: var(--bg3);
    border-radius: 6px;
    border: 2px solid var(--bg1);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--bg4);
}

/* Column spacing */
.gr-column {
    padding: 12px !important;
}

/* Remove default Gradio styling */
.gr-box {
    border: none !important;
    background: transparent !important;
}

/* Info boxes */
.info-box {
    background: var(--bg-blue) !important;
    border-left: 3px solid var(--blue) !important;
    padding: 12px 16px !important;
    border-radius: 4px !important;
    margin: 12px 0 !important;
}

/* Warning boxes */
.warning-box {
    background: var(--bg-yellow) !important;
    border-left: 3px solid var(--yellow) !important;
}

/* Success boxes */
.success-box {
    background: var(--bg-green) !important;
    border-left: 3px solid var(--green) !important;
}

/* Error boxes */
.error-box {
    background: var(--bg-red) !important;
    border-left: 3px solid var(--red) !important;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid var(--bg3) !important;
    margin: 24px 0 !important;
}

/* Labels */
label {
    color: var(--grey2) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
    display: block;
}

/* Examples */
.examples {
    background: var(--bg1) !important;
    border: 1px solid var(--bg3) !important;
    border-radius: 4px !important;
}
"""

def query_vllm_stream(port: str, prompt: str, max_tokens: int = 100):
    """Query a vLLM endpoint with streaming and yield chunks"""
    if ':' in port:
        base_url = f"http://{port}"
    else:
        base_url = f"http://localhost:{port}"

    try:
        models_response = requests.get(f"{base_url}/v1/models", timeout=5)
        if models_response.status_code == 200:
            model_name = models_response.json()['data'][0]['id']
        else:
            model_name = "deployed-model"
    except:
        model_name = "deployed-model"

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
        yield f"Connection error: Cannot reach {endpoint}", {}
    except Exception as e:
        yield f"Error: {str(e)}", {}

def format_output(text: str, metrics: dict = None, status: str = "running"):
    """Format output with metrics"""
    if not text:
        return f"*Status: {status}... waiting for response*"

    output = f"{text}\n\n"

    if metrics:
        output += f"---\n\n"
        output += f"**Performance Metrics**\n\n"
        output += f"| Metric | Value |\n"
        output += f"|--------|-------|\n"
        output += f"| Latency | {metrics['latency_ms']} ms |\n"
        output += f"| Throughput | {metrics['tokens_per_sec']} tokens/sec |\n"
        output += f"| Tokens | {metrics['tokens']} |\n"
    else:
        output += f"\n*{status}...*\n"

    return output

def compare_models(prompt: str, original_port: str, quantized_port: str, max_tokens: int):
    """Compare responses from both models with concurrent streaming"""

    if not prompt.strip():
        yield "Please enter a prompt", "", ""
        return

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

    orig_thread = threading.Thread(target=stream_original)
    quant_thread = threading.Thread(target=stream_quantized)

    orig_thread.start()
    quant_thread.start()

    while not (state['orig_done'] and state['quant_done']):
        orig_result = format_output(
            state['orig_text'],
            state['orig_metrics'],
            "complete" if state['orig_done'] else "generating"
        )
        quant_result = format_output(
            state['quant_text'],
            state['quant_metrics'],
            "complete" if state['quant_done'] else "generating"
        )

        yield orig_result, quant_result, ""
        time.sleep(0.1)

    orig_thread.join()
    quant_thread.join()

    orig_result = format_output(state['orig_text'], state['orig_metrics'], "complete")
    quant_result = format_output(state['quant_text'], state['quant_metrics'], "complete")

    if state['orig_metrics'] and state['quant_metrics']:
        speedup = state['quant_metrics']['tokens_per_sec'] / state['orig_metrics']['tokens_per_sec']
        latency_reduction = ((state['orig_metrics']['latency_ms'] - state['quant_metrics']['latency_ms']) / state['orig_metrics']['latency_ms']) * 100

        summary = f"""
## Benchmark Results

**Performance Improvement:** {speedup:.2f}x speedup · {abs(latency_reduction):.1f}% {'faster' if latency_reduction > 0 else 'slower'} latency

| Metric | Original (FP16) | Quantized (INT4) | Improvement |
|--------|----------------|------------------|-------------|
| Latency | {state['orig_metrics']['latency_ms']} ms | {state['quant_metrics']['latency_ms']} ms | {abs(latency_reduction):.1f}% |
| Throughput | {state['orig_metrics']['tokens_per_sec']} tok/s | {state['quant_metrics']['tokens_per_sec']} tok/s | {speedup:.2f}x |
| Tokens Generated | {state['orig_metrics']['tokens']} | {state['quant_metrics']['tokens']} | same |

Compare the response quality above to evaluate any degradation from quantization.
"""
    else:
        summary = "⚠️ Comparison failed - one or both models did not respond"

    yield orig_result, quant_result, summary

# Gradio UI with Everforest theme
with gr.Blocks(css=EVERFOREST_CSS, title="LLM Quantization Comparison") as demo:
    gr.Markdown("""
    # LLM Quantization Comparison

    Compare original vs quantized model performance side-by-side with concurrent execution.

    **Boston Tech Week 2026** · Model Compression Workshop
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Configuration")
            original_port = gr.Textbox(
                label="Original Model Endpoint",
                value="vllm-original:8080",
                placeholder="hostname:port"
            )
            quantized_port = gr.Textbox(
                label="Quantized Model Endpoint",
                value="vllm-quantized:8081",
                placeholder="hostname:port"
            )
            max_tokens = gr.Slider(
                minimum=50,
                maximum=500,
                value=100,
                step=10,
                label="Max Tokens",
            )

    gr.Markdown("### Prompt")
    prompt = gr.Textbox(
        label="Enter your prompt",
        placeholder="Type your prompt here or select an example below...",
        lines=3
    )

    compare_btn = gr.Button("Compare Models", variant="primary", size="lg")

    gr.Markdown("---")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Original Model (FP16)")
            original_output = gr.Markdown()

        with gr.Column():
            gr.Markdown("### Quantized Model (INT4)")
            quantized_output = gr.Markdown()

    gr.Markdown("---")

    comparison_summary = gr.Markdown()

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

### Usage

1. Configure vLLM endpoints above (defaults are pre-set)
2. Enter a prompt or select an example
3. Click "Compare Models" to run both concurrently
4. Observe real-time generation and metrics

### What to Look For

- **Throughput gains** – Quantized models typically achieve 1.5-2x speedup
- **Latency reduction** – 30-50% faster response times
- **Output quality** – Compare responses to assess any degradation
- **Memory efficiency** – INT4 uses ~75% less VRAM than FP16
    """)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
