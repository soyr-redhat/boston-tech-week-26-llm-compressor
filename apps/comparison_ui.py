#!/usr/bin/env python3
"""
vLLM Model Comparison - Red Hat Theme
Boston Tech Week 2026 - LLM Quantization Workshop
"""

import gradio as gr
import requests
import time
import json
import threading
from typing import Dict, Tuple

# Red Hat Theme CSS
REDHAT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Mono:wght@400;500;600&family=Red+Hat+Text:wght@400;500;600;700&display=swap');

:root {
    --bg0: #1a1a1a;
    --bg1: #242424;
    --bg2: #2e2e2e;
    --bg3: #383838;
    --bg4: #424242;
    --fg: #f5f5f5;
    --red: #ee0000;
    --red-dark: #a60000;
    --red-darker: #5f0000;
    --grey0: #6a6a6a;
    --grey1: #8a8a8a;
    --grey2: #aaaaaa;
}

* {
    box-sizing: border-box;
}

body, .gradio-container {
    background: var(--bg0) !important;
    font-family: 'Red Hat Text', system-ui, sans-serif !important;
    color: var(--fg) !important;
    line-height: 1.5;
    padding: 0 !important;
    margin: 0 !important;
}

/* Compact main container */
#component-0, .contain, .wrap {
    background: var(--bg0) !important;
    border: none !important;
    padding: 16px !important;
    max-width: 100% !important;
}

.gradio-container {
    max-width: 100% !important;
    padding: 8px !important;
}

/* Compact headers */
h1, h2, h3, h4 {
    font-family: 'Red Hat Text', sans-serif !important;
    font-weight: 600 !important;
    margin: 0 0 8px 0 !important;
    padding: 0 !important;
    line-height: 1.3 !important;
}

h1 {
    font-size: 1.4rem !important;
    color: var(--red) !important;
    border-bottom: 1px solid var(--bg3);
    padding-bottom: 8px !important;
    margin-bottom: 12px !important;
}

h2 {
    font-size: 1.1rem !important;
    color: var(--grey2) !important;
}

h3 {
    font-size: 0.95rem !important;
    color: var(--grey1) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

p, span, label, .prose {
    color: var(--fg) !important;
    font-family: 'Red Hat Text', sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
}

.prose p {
    margin: 4px 0 !important;
}

code, pre {
    font-family: 'Red Hat Mono', monospace !important;
    background: var(--bg1) !important;
    color: var(--fg) !important;
    font-size: 0.9em !important;
}

pre {
    border: 1px solid var(--bg4) !important;
    border-radius: 3px !important;
    padding: 8px !important;
    margin: 4px 0 !important;
}

code {
    padding: 2px 4px !important;
    border-radius: 2px !important;
}

/* Compact inputs with darker borders */
input[type="text"], textarea {
    background: var(--bg1) !important;
    border: 2px solid var(--bg4) !important;
    border-radius: 3px !important;
    color: var(--fg) !important;
    padding: 6px 10px !important;
    margin: 0 !important;
    font-size: 0.9rem !important;
}

input:focus, textarea:focus {
    border-color: var(--red) !important;
    outline: none !important;
}

textarea {
    min-height: 60px !important;
}

/* Compact buttons */
button {
    background: var(--bg2) !important;
    border: 1px solid var(--red) !important;
    color: var(--red) !important;
    font-family: 'Red Hat Text', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    border-radius: 3px !important;
    font-size: 0.9rem !important;
    margin: 4px 0 !important;
}

button:hover {
    background: var(--red) !important;
    color: white !important;
}

.primary {
    background: var(--red) !important;
    color: white !important;
}

/* Output areas with scrolling and darker borders */
.markdown-output, .output-markdown {
    background: var(--bg1) !important;
    border: 2px solid var(--bg4) !important;
    border-radius: 3px !important;
    padding: 10px !important;
    color: var(--fg) !important;
    min-height: 300px !important;
    max-height: 500px !important;
    overflow-y: auto !important;
    font-size: 0.9rem !important;
}

/* Compact slider */
.slider-container {
    padding: 4px 0 !important;
}

/* Compact tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0 !important;
    font-size: 0.85rem !important;
}

th, td {
    border: 1px solid var(--bg3) !important;
    padding: 6px 8px !important;
    color: var(--fg) !important;
}

th {
    background: var(--bg2) !important;
    color: var(--red) !important;
    font-weight: 600;
}

strong {
    color: var(--red) !important;
}

/* Compact rows and columns */
.gr-row {
    gap: 12px !important;
    margin: 0 !important;
}

.gr-column {
    padding: 0 !important;
    margin: 0 !important;
}

.gr-form {
    gap: 8px !important;
}

.gr-box {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Compact labels */
label {
    color: var(--grey2) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
    display: block;
}

/* Remove excessive padding */
.block {
    padding: 0 !important;
    margin: 0 !important;
}

.panel {
    padding: 8px !important;
}

/* Compact horizontal rules */
hr {
    border: none;
    border-top: 1px solid var(--bg3) !important;
    margin: 12px 0 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg1);
}

::-webkit-scrollbar-thumb {
    background: var(--bg3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--bg4);
}

/* Compact examples */
.examples {
    margin: 8px 0 !important;
}

/* Remove default spacing */
.gap {
    gap: 8px !important;
}

/* Hide settings button and theme selector */
.settings-button, button[aria-label*="settings"], button[aria-label*="Settings"],
footer, .footer, #footer, [id*="settings"], [class*="settings-btn"] {
    display: none !important;
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

    # Use chat completions API for proper instruct formatting
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": True
    }

    url = f"{base_url}/v1/chat/completions"

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
                            # Chat completions use delta.content instead of text
                            delta_obj = data['choices'][0].get('delta', {})
                            delta = delta_obj.get('content', '')
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

def format_output(text: str, metrics: dict = None):
    """Format output with inline metrics"""
    if not text:
        return "*waiting...*"

    output = f"{text}\n"

    if metrics:
        output += f"\n**Metrics:** {metrics['latency_ms']}ms · {metrics['tokens_per_sec']} tok/s · {metrics['tokens']} tokens"

    return output

def compare_models(prompt: str, original_port: str, quantized_port: str, max_tokens: int):
    """Compare responses from both models with concurrent streaming"""

    if not prompt.strip():
        yield "Enter a prompt", "", ""
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
        orig_result = format_output(state['orig_text'], state['orig_metrics'])
        quant_result = format_output(state['quant_text'], state['quant_metrics'])

        yield orig_result, quant_result, ""
        time.sleep(0.1)

    orig_thread.join()
    quant_thread.join()

    orig_result = format_output(state['orig_text'], state['orig_metrics'])
    quant_result = format_output(state['quant_text'], state['quant_metrics'])

    if state['orig_metrics'] and state['quant_metrics']:
        speedup = state['quant_metrics']['tokens_per_sec'] / state['orig_metrics']['tokens_per_sec']
        latency_diff = state['orig_metrics']['latency_ms'] - state['quant_metrics']['latency_ms']

        summary = f"""**Result:** {speedup:.2f}x speedup · {latency_diff:.0f}ms faster

| Metric | Original | Quantized | Δ |
|--------|----------|-----------|---|
| Latency | {state['orig_metrics']['latency_ms']}ms | {state['quant_metrics']['latency_ms']}ms | {latency_diff:.0f}ms |
| Throughput | {state['orig_metrics']['tokens_per_sec']} tok/s | {state['quant_metrics']['tokens_per_sec']} tok/s | {speedup:.2f}x |
| Tokens | {state['orig_metrics']['tokens']} | {state['quant_metrics']['tokens']} | — |
"""
    else:
        summary = "Error: comparison failed"

    yield orig_result, quant_result, summary

# Compact Gradio UI - outputs first, then input
with gr.Blocks(
    title="LLM Quantization",
    head='<link rel="icon" type="image/svg+xml" href="https://soyr-redhat.github.io/boston-tech-week-26-llm-compressor/assets/redhat.svg">'
) as demo:
    gr.Markdown("# LLM Quantization Comparison")

    # Output windows FIRST
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Original (FP16)")
            original_output = gr.Markdown()
        with gr.Column():
            gr.Markdown("## Quantized (INT4)")
            quantized_output = gr.Markdown()

    comparison_summary = gr.Markdown()

    # Input section BELOW outputs
    with gr.Row():
        prompt = gr.Textbox(
            label="Prompt",
            placeholder="Enter prompt...",
            lines=2,
            scale=3
        )
        with gr.Column(scale=1):
            max_tokens = gr.Slider(50, 500, 100, step=10, label="Tokens")
            compare_btn = gr.Button("Compare", variant="primary")

    with gr.Accordion("Configuration", open=False):
        with gr.Row():
            original_port = gr.Textbox(
                label="Original",
                value="vllm-original:8080",
                scale=1
            )
            quantized_port = gr.Textbox(
                label="Quantized",
                value="vllm-quantized:8081",
                scale=1
            )

    gr.Examples(
        examples=[
            ["The future of artificial intelligence is", "vllm-original:8080", "vllm-quantized:8081", 100],
            ["Write a Python function to sort a list", "vllm-original:8080", "vllm-quantized:8081", 150],
            ["Explain quantum computing", "vllm-original:8080", "vllm-quantized:8081", 200],
        ],
        inputs=[prompt, original_port, quantized_port, max_tokens],
        label="Examples"
    )

    compare_btn.click(
        fn=compare_models,
        inputs=[prompt, original_port, quantized_port, max_tokens],
        outputs=[original_output, quantized_output, comparison_summary]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        css=REDHAT_CSS
    )
