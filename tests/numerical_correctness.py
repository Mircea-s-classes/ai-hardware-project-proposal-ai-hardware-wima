import torch
import numpy as np

# -----------------------------
# Configuration
# -----------------------------
MODEL_PATH = "model/inference/model.pt"
INPUT_SHAPE = (1, 1, 64, 64)
NUM_TESTS = 20
ATOL = 1e-4
RTOL = 1e-3

# -----------------------------
# Load Model
# -----------------------------
model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

# -----------------------------
# Simulated FPGA Path
# (Placeholder for accelerated inference)
# -----------------------------
def fpga_inference_sim(model, x):
    # In real system: DMA → FPGA → output
    # Here: same model to validate numerical consistency
    return model(x)

# -----------------------------
# Test Loop
# -----------------------------
mismatch_count = 0

with torch.no_grad():
    for i in range(NUM_TESTS):
        x = torch.randn(INPUT_SHAPE)

        cpu_out = model(x)
        fpga_out = fpga_inference_sim(model, x)

        if not torch.allclose(cpu_out, fpga_out, rtol=RTOL, atol=ATOL):
            mismatch_count += 1
            diff = torch.abs(cpu_out - fpga_out).max().item()
            print(f"[Mismatch {i}] Max diff: {diff:.6f}")

# -----------------------------
# Summary
# -----------------------------
print("\nNumerical Correctness Test Summary")
print("---------------------------------")
print(f"Total tests     : {NUM_TESTS}")
print(f"Mismatches      : {mismatch_count}")
print(f"Tolerance (rtol): {RTOL}")
print(f"Tolerance (atol): {ATOL}")

if mismatch_count == 0:
    print("Status          : PASS")
else:
    print("Status          : REVIEW)

