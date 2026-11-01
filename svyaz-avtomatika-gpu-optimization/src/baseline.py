import time
import torch
from tqdm import tqdm
from model import load_model, get_dummy_input

def run_baseline(batch_size: int = 1, iterations: int = 100) -> tuple:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_model(device, optimize=False)
    x = get_dummy_input(batch_size, device, optimize=False)

    with torch.no_grad():
        for _ in range(10):
            _ = model(x)
    if device.type == 'cuda':
        torch.cuda.synchronize()

    times = []
    with torch.no_grad():
        for _ in tqdm(range(iterations), desc="Baseline (FP32)"):
            start = time.perf_counter()
            _ = model(x)
            if device.type == 'cuda':
                torch.cuda.synchronize()
            times.append(time.perf_counter() - start)

    avg_time = sum(times) / len(times)
    return (avg_time * 1000, batch_size / avg_time)