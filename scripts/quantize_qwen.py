#!/usr/bin/env python3
"""
Quantize Qwen2.5-0.5B using llm-compressor

Usage:
    python quantize_qwen.py --bits 4 --output ./qwen2.5-0.5b-gptq-int4
    python quantize_qwen.py --bits 8 --output ./qwen2.5-0.5b-gptq-int8
"""

import argparse
import time
from datasets import load_dataset
from llmcompressor.transformers import oneshot


def create_recipe(num_bits=4):
    """Create GPTQ quantization recipe"""
    return f"""
quant_stage:
    quant_modifiers:
        GPTQModifier:
            sequential_update: false
            ignore: ["lm_head"]
            config_groups:
                group_0:
                    weights:
                        num_bits: {num_bits}
                        type: "int"
                        symmetric: true
                        strategy: "channel"
                    targets: ["Linear"]
"""


def load_calibration_data(num_samples=256):
    """Load calibration dataset from C4"""
    print(f"Loading {num_samples} calibration samples from C4...")
    dataset = load_dataset(
        "allenai/c4",
        data_files="en/c4-train.00000-of-01024.json.gz",
        split="train"
    ).select(range(num_samples))
    print(f"✓ Loaded {len(dataset)} samples")
    return dataset


def main():
    parser = argparse.ArgumentParser(description="Quantize Qwen2.5-0.5B")
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen2.5-0.5B",
        help="Model ID from HuggingFace"
    )
    parser.add_argument(
        "--bits",
        type=int,
        choices=[4, 8],
        default=4,
        help="Quantization bits (4 or 8)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./qwen2.5-0.5b-gptq-int4",
        help="Output directory for quantized model"
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=256,
        help="Number of calibration samples"
    )
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=2048,
        help="Maximum sequence length"
    )
    args = parser.parse_args()

    print("="*60)
    print(f"Quantizing {args.model} to INT{args.bits}")
    print("="*60)

    # Create recipe
    recipe = create_recipe(args.bits)
    print(f"\nRecipe: INT{args.bits} GPTQ")

    # Load calibration data
    calibration_dataset = load_calibration_data(args.num_samples)

    # Run quantization
    print(f"\nStarting quantization...")
    print(f"  Output: {args.output}")
    print(f"  Calibration samples: {args.num_samples}")
    print(f"  Max sequence length: {args.max_seq_length}\n")

    start_time = time.time()

    oneshot(
        model=args.model,
        dataset=calibration_dataset,
        recipe=recipe,
        output_dir=args.output,
        max_seq_length=args.max_seq_length,
        num_calibration_samples=args.num_samples,
    )

    elapsed = time.time() - start_time

    print("\n" + "="*60)
    print(f"✓ Quantization complete!")
    print(f"  Time: {elapsed:.1f} seconds")
    print(f"  Output: {args.output}")
    print("="*60)


if __name__ == "__main__":
    main()
