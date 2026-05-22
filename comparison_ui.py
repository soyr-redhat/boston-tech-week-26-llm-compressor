#!/usr/bin/env python3
"""
Terminal-Style vLLM Model Comparison
Boston Tech Week 2026 - LLM Quantization Workshop
"""

import gradio as gr
import requests
import time
import json
import threading
from typing import Dict, Tuple

# Terminal-style custom CSS with retro CRT phosphor aesthetic
TERMINAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --phosphor-green: #00ff41;
    --phosphor-dim: #00cc33;
    --screen-bg: #0a0e0a;
    --terminal-bg: #0d1117;
    --cursor-color: #00ff41;
}

body, .gradio-container {
    background: var(--screen-bg) !important;
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: var(--phosphor-green) !important;
}

/* CRT screen effect */
.gradio-container::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15),
        rgba(0, 0, 0, 0.15) 1px,
        transparent 1px,
        transparent 2px
    );
    pointer-events: none;
    z-index: 1000;
}

/* Phosphor glow effect */
.gradio-container::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 255, 65, 0.03) 100%);
    pointer-events: none;
    z-index: 999;
}

/* Main container styling */
#component-0, .contain, .wrap {
    background: var(--terminal-bg) !important;
    border: 2px solid var(--phosphor-dim) !important;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.3), inset 0 0 30px rgba(0, 255, 65, 0.05) !important;
    border-radius: 8px !important;
}

/* Text elements */
.prose, .markdown, p, h1, h2, h3, h4, label, span {
    color: var(--phosphor-green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-shadow: 0 0 5px rgba(0, 255, 65, 0.5);
}

h1 {
    font-size: 1.8rem !important;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-bottom: 2px solid var(--phosphor-dim);
    padding-bottom: 10px;
    margin-bottom: 20px !important;
}

h2, h3 {
    color: var(--phosphor-green) !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Input fields */
input, textarea, .input-text {
    background: #000 !important;
    border: 1px solid var(--phosphor-dim) !important;
    color: var(--phosphor-green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.1) !important;
    caret-color: var(--cursor-color);
}

input:focus, textarea:focus {
    border-color: var(--phosphor-green) !important;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.4) !important;
    outline: none !important;
}

/* Buttons */
button {
    background: var(--terminal-bg) !important;
    border: 2px solid var(--phosphor-green) !important;
    color: var(--phosphor-green) !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    transition: all 0.2s;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
}

button:hover {
    background: var(--phosphor-green) !important;
    color: #000 !important;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
    transform: translateY(-2px);
}

/* Output boxes */
.markdown-output, .output-markdown {
    background: #000 !important;
    border: 1px solid var(--phosphor-dim) !important;
    padding: 15px !important;
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--phosphor-green) !important;
    min-height: 200px;
    box-shadow: inset 0 0 15px rgba(0, 255, 65, 0.1);
}

/* Slider */
input[type="range"] {
    accent-color: var(--phosphor-green);
}

/* Code blocks */
code, pre {
    background: #000 !important;
    color: var(--phosphor-green) !important;
    border: 1px solid var(--phosphor-dim) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Tables */
table {
    border-collapse: collapse;
    color: var(--phosphor-green) !important;
}

th, td {
    border: 1px solid var(--phosphor-dim) !important;
    padding: 8px !important;
    color: var(--phosphor-green) !important;
}

th {
    background: rgba(0, 255, 65, 0.1) !important;
    font-weight: 700;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #000;
}

::-webkit-scrollbar-thumb {
    background: var(--phosphor-dim);
    border: 1px solid var(--phosphor-green);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--phosphor-green);
}

/* Remove emojis effect for cleaner terminal look */
.prose strong::before {
    content: "[" !important;
}

.prose strong::after {
    content: "]" !important;
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
            yield f"[ERROR {response.status_code}] {response.text}", {}
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
        yield f"[CONNECTION ERROR] Cannot reach {endpoint}", {}
    except Exception as e:
        yield f"[ERROR] {str(e)}", {}

def format_terminal_output(text: str, metrics: dict = None, status: str = "RUNNING"):
    """Format output in terminal style with ASCII box drawing"""
    if not text:
        return f"[{status}] Awaiting response..."

    output = f"```\n{text}\n```\n"

    if metrics:
        output += f"\n╔═══════════════════════════════════════╗\n"
        output += f"║ PERFORMANCE METRICS                   ║\n"
        output += f"╠═══════════════════════════════════════╣\n"
        output += f"║ LATENCY     : {metrics['latency_ms']:>8} ms          ║\n"
        output += f"║ THROUGHPUT  : {metrics['tokens_per_sec']:>8} tok/s       ║\n"
        output += f"║ TOKENS      : {metrics['tokens']:>8}              ║\n"
        output += f"╚═══════════════════════════════════════╝\n"
    else:
        output += f"\n[{status}] Generating...\n"

    return output

def compare_models(prompt: str, original_port: str, quantized_port: str, max_tokens: int):
    """Compare responses from both models with concurrent streaming"""

    if not prompt.strip():
        yield "[ERROR] Prompt required", "", ""
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
        orig_result = format_terminal_output(
            state['orig_text'],
            state['orig_metrics'],
            "COMPLETE" if state['orig_done'] else "RUNNING"
        )
        quant_result = format_terminal_output(
            state['quant_text'],
            state['quant_metrics'],
            "COMPLETE" if state['quant_done'] else "RUNNING"
        )

        yield orig_result, quant_result, ""
        time.sleep(0.1)

    orig_thread.join()
    quant_thread.join()

    orig_result = format_terminal_output(state['orig_text'], state['orig_metrics'], "COMPLETE")
    quant_result = format_terminal_output(state['quant_text'], state['quant_metrics'], "COMPLETE")

    if state['orig_metrics'] and state['quant_metrics']:
        speedup = state['quant_metrics']['tokens_per_sec'] / state['orig_metrics']['tokens_per_sec']
        latency_reduction = ((state['orig_metrics']['latency_ms'] - state['quant_metrics']['latency_ms']) / state['orig_metrics']['latency_ms']) * 100

        summary = f"""
```
╔═══════════════════════════════════════════════════════════════════╗
║                    BENCHMARK COMPARISON RESULTS                   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  SPEEDUP FACTOR      : {speedup:.2f}x                                        ║
║  LATENCY IMPROVEMENT : {abs(latency_reduction):.1f}% {'faster' if latency_reduction > 0 else 'slower'}                                  ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║  METRIC       │ ORIGINAL (FP16) │ QUANTIZED (INT4) │ DIFFERENCE  ║
╠═══════════════════════════════════════════════════════════════════╣
║  Latency      │ {state['orig_metrics']['latency_ms']:>8} ms     │ {state['quant_metrics']['latency_ms']:>9} ms    │ {abs(latency_reduction):>6.1f}%     ║
║  Throughput   │ {state['orig_metrics']['tokens_per_sec']:>8} tok/s  │ {state['quant_metrics']['tokens_per_sec']:>9} tok/s │ {speedup:>6.2f}x     ║
║  Tokens       │ {state['orig_metrics']['tokens']:>8}        │ {state['quant_metrics']['tokens']:>9}       │   SAME      ║
╚═══════════════════════════════════════════════════════════════════╝
```

**ANALYSIS:** Quantization achieved **{speedup:.2f}x** throughput improvement with **{abs(latency_reduction):.1f}%** latency reduction.
Compare output quality above to assess any degradation from compression.
"""
    else:
        summary = "[ERROR] Comparison failed - one or both models did not respond"

    yield orig_result, quant_result, summary

# Terminal-themed Gradio UI
with gr.Blocks(css=TERMINAL_CSS, title="LLM QUANTIZATION TERMINAL") as demo:
    gr.Markdown("""
    # ┌─ BOSTON TECH WEEK 2026 ─────────────────────────────────┐
    # │ LLM QUANTIZATION BENCHMARK TERMINAL                     │
    # └─────────────────────────────────────────────────────────┘

    **SYSTEM:** Side-by-side model comparison interface
    **MODE:** Concurrent execution with real-time metrics
    **MODELS:** FP16 baseline vs INT4 quantized
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ┌─ SERVER CONFIGURATION ─┐")
            original_port = gr.Textbox(
                label="[ORIGINAL] Model Endpoint",
                value="vllm-original:8080",
                placeholder="hostname:port"
            )
            quantized_port = gr.Textbox(
                label="[QUANTIZED] Model Endpoint",
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

    gr.Markdown("### ┌─ PROMPT INPUT ─┐")
    prompt = gr.Textbox(
        label="[PROMPT]",
        placeholder="> Enter your prompt here...",
        lines=3
    )

    compare_btn = gr.Button("[ EXECUTE BENCHMARK ]", variant="primary", size="lg")

    gr.Markdown("```\n────────────────────────────────────────────────────────────────\n```")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### ┌─ ORIGINAL MODEL (FP16) ─┐")
            original_output = gr.Markdown()

        with gr.Column():
            gr.Markdown("### ┌─ QUANTIZED MODEL (INT4) ─┐")
            quantized_output = gr.Markdown()

    gr.Markdown("```\n────────────────────────────────────────────────────────────────\n```")

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
```
────────────────────────────────────────────────────────────────
 USAGE INSTRUCTIONS
────────────────────────────────────────────────────────────────
 1. Configure vLLM server endpoints above
 2. Enter prompt or select example
 3. Execute benchmark for concurrent comparison
 4. Analyze throughput delta and quality metrics
────────────────────────────────────────────────────────────────
 SYSTEM STATUS: READY
────────────────────────────────────────────────────────────────
```
    """)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
