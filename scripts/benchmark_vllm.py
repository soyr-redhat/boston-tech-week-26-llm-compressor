#!/usr/bin/env python3
"""
Benchmark vLLM inference for original vs quantized models

Usage:
    python benchmark_vllm.py --original Qwen/Qwen2.5-0.5B --quantized ./qwen2.5-0.5b-gptq-int4
"""

import argparse
import time
from vllm import LLM, SamplingParams


TEST_PROMPTS = [
    "The future of artificial intelligence is",
    "Machine learning models are",
    "Quantum computing will",
    "The key to sustainable energy is",
    "The most important skill for a developer is",
    "Open source software enables",
    "Cloud computing has transformed",
    "The challenge with large language models is",
    "In the next decade, we will see",
    "The relationship between humans and AI will",
]


def benchmark_model(model_path, quantization=None, num_prompts=50):
    """Benchmark a model with vLLM"""
    print(f"\nLoading model: {model_path}")
    if quantization:
        print(f"  Quantization: {quantization}")

    llm = LLM(
        model=model_path,
        quantization=quantization,
        gpu_memory_utilization=0.4,
    )

    sampling_params = SamplingParams(
        temperature=0.7,
        top_p=0.9,
        max_tokens=100,
    )

    # Generate prompts
    prompts = (TEST_PROMPTS * (num_prompts // len(TEST_PROMPTS) + 1))[:num_prompts]

    print(f"  Running {len(prompts)} prompts...")
    start = time.time()
    outputs = llm.generate(prompts, sampling_params)
    elapsed = time.time() - start

    throughput = len(prompts) / elapsed
    latency = elapsed / len(prompts)

    return {
        "time": elapsed,
        "throughput": throughput,
        "latency": latency,
        "num_prompts": len(prompts),
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark vLLM models")
    parser.add_argument(
        "--original",
        type=str,
        default="Qwen/Qwen2.5-0.5B",
        help="Original model path"
    )
    parser.add_argument(
        "--quantized",
        type=str,
        default="./qwen2.5-0.5b-gptq-int4",
        help="Quantized model path"
    )
    parser.add_argument(
        "--num-prompts",
        type=int,
        default=50,
        help="Number of prompts to benchmark"
    )
    args = parser.parse_args()

    print("="*60)
    print("vLLM BENCHMARK")
    print("="*60)

    # Benchmark original
    print("\n[1/2] Benchmarking ORIGINAL model...")
    results_original = benchmark_model(args.original, num_prompts=args.num_prompts)

    # Benchmark quantized
    print("\n[2/2] Benchmarking QUANTIZED model...")
    results_quantized = benchmark_model(
        args.quantized,
        quantization="gptq",
        num_prompts=args.num_prompts
    )

    # Print results
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"\nOriginal Model ({args.original}):")
    print(f"  Total time:       {results_original['time']:.2f}s")
    print(f"  Throughput:       {results_original['throughput']:.2f} req/s")
    print(f"  Avg latency:      {results_original['latency']*1000:.1f} ms/req")

    print(f"\nQuantized Model ({args.quantized}):")
    print(f"  Total time:       {results_quantized['time']:.2f}s")
    print(f"  Throughput:       {results_quantized['throughput']:.2f} req/s")
    print(f"  Avg latency:      {results_quantized['latency']*1000:.1f} ms/req")

    speedup = results_quantized['throughput'] / results_original['throughput']
    print(f"\nSpeedup: {speedup:.2f}x")
    print("="*60)


if __name__ == "__main__":
    main()
