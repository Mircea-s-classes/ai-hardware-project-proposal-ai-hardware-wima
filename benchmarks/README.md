# Benchmarking

This directory contains scripts used to evaluate inference performance
and throughput for the ASL recognition system.

## Scripts
- `latency_cpu.py`: Measures CPU-only inference latency and FPS
- `latency_fpga_sim.py`: Simulated accelerated inference path for comparison

Benchmarks are conducted using repeated inference runs and warm-up cycles
to ensure fair timing measurements.
