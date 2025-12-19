# Figures

This directory contains all figures used throughout the main project README, the LaTeX final report, and the course presentations.  
These figures document **model accuracy**, **latency and throughput benchmarks**, and the **hardware–software co-design architecture** implemented in this project.

---

## Model Training and Accuracy

These figures summarize CNN training behavior and final classification performance:

- **Accuracy.png**  
  Training and validation accuracy versus epoch, demonstrating convergence and generalization.

- **Accuracy_Benchmark.png**  
  Final top-1 classification accuracy comparison between:
  - CPU-only inference
  - CPU + FPGA accelerated inference  
  This confirms that hardware acceleration does **not degrade accuracy**.

---

## Inference Latency and Performance Benchmarks

These figures evaluate real-time inference performance under batch size = 1:

- **CPU_Latency.png**  
  Mean CPU inference latency with standard deviation (FP32 execution).

- **Inference_Latency_Benchmark.png**  
  Direct comparison of inference latency between:
  - CPU-only execution
  - CPU + FPGA accelerated execution  
  This demonstrates a significant reduction in latency when offloading convolution to the FPGA.

- **Latency-Distribution.png**  
  Histogram of CPU inference latency showing variance and tail behavior, highlighting the benefit of FPGA acceleration for consistent real-time performance.

---

## Hardware–Software Co-Design Architecture

These figures document the system-level architecture and FPGA implementation flow:

- **asl_cnn_fpga_split.png**  
  End-to-end system diagram illustrating the CNN partitioning:
  - First convolution layer accelerated in FPGA programmable logic (PL)
  - Remaining layers executed on the ARM processing system (PS)

- **vitis_hls_asl_conv1_screenshot.png**  
  Vitis HLS synthesis report for the `asl_conv1` accelerator, including latency estimates and resource utilization.

- **vivado_bd_asl_system.png**  
  Vivado block design showing integration of:
  - Zynq processing system
  - AXI interconnect
  - Custom HLS convolution IP core

- **vivado_implementation_success.png**  
  Successful FPGA implementation and placement view, confirming timing closure and correct integration.

---

## Usage Notes

- All benchmarks were collected using **batch size = 1** to reflect real-time inference.
- CPU and FPGA measurements use the **same trained model and input resolution**.
- Figures are referenced directly in:
  - Main project `README.md`
  - LaTeX final report
  - Midterm and final presentations

This directory serves as the **visual evidence** supporting the performance and design claims made throughout the project.
