import time
import numpy as np
import torch

# -----------------------------
# Configuration
# -----------------------------
MODEL_PATH = "model/inference/model.pt"   # UPDATE if needed
INPUT_SHAPE = (1, 1, 64, 64)               # Example ASL input
NUM_RUNS = 100
WARMUP_RUNS = 10
DEVICE = "cpu"

# -----------------------------
# Load Model
# -----------------------------
model = torch.load(MODEL_PATH, map_location=DEVICE)
model.eval()

# Dummy input (replace with real preprocessed sample if available)
dummy_input = torch.randn(INPUT_SHAPE)

# -----------------------------
# Warm-up (important for fair timing)
# -----------------------------
with torch.no_grad():
    for _ in range(WARMUP_RUNS):
        _ = model(dummy_input)

# -----------------------------
# Benchmark
# -----------------------------
latencies = []

with torch.no_grad():
    for _ in range(NUM_RUNS):
        start = time.perf_counter()
        _ = model(dummy_input)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)  # ms

latencies = np.array(latencies)

# -----------------------------
# Results
# -----------------------------
print("CPU Inference Benchmark Results")
print("--------------------------------")
print(f"Runs           : {NUM_RUNS}")
print(f"Avg Latency ms : {latencies.mean():.2f}")
print(f"Min Latency ms : {latencies.min():.2f}")
print(f"Max Latency ms : {latencies.max():.2f}")
print(f"FPS (avg)      : {1000 / latencies.mean():.2f}")

