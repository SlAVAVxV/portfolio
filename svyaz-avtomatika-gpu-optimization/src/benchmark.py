import argparse
import torch
from baseline import run_baseline
from optimized import run_optimized

def main():
    parser = argparse.ArgumentParser(description="Сравнение инференса ResNet-50 на GPU")
    parser.add_argument("--batch-size", type=int, default=1, help="Размер батча")
    parser.add_argument("--iterations", type=int, default=100, help="Количество итераций")
    args = parser.parse_args()

    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU (GPU не обнаружен)"
    print(f"=== Batch Size = {args.batch_size} | Устройство: {device_name} ===\n")

    mem_before = torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0
    base_ms, base_fps = run_baseline(args.batch_size, args.iterations)
    mem_base = (torch.cuda.max_memory_allocated() - mem_before) / (1024**2) if torch.cuda.is_available() else 0

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    mem_before = torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0
    opt_ms, opt_fps = run_optimized(args.batch_size, args.iterations)
    mem_opt = (torch.cuda.max_memory_allocated() - mem_before) / (1024**2) if torch.cuda.is_available() else 0

    print("\n" + "="*55)
    print(f"{'Метрика':<28} | {'Baseline':<10} | {'Optimized':<10}")
    print("-" * 55)
    print(f"{'Latency (ms)':<28} | {base_ms:<10.2f} | {opt_ms:<10.2f}")
    print(f"{'Throughput (FPS)':<28} | {base_fps:<10.1f} | {opt_fps:<10.1f}")
    if torch.cuda.is_available():
        print(f"{'Peak VRAM (MB)':<28} | {mem_base:<10.0f} | {mem_opt:<10.0f}")
    print("="*55)
    print(f"Ускорение по latency: {base_ms / opt_ms:.2f}x\n")

if __name__ == "__main__":
    main()