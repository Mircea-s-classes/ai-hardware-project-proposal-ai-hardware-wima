# Hardware Integration (`src/hardware/`)

This directory contains the **hardware–software interface code** used to deploy and control the trained CNN model on FPGA hardware using the **ZtaChip accelerator**.

It represents the **runtime execution layer** of the AI system.

---

## Purpose

The purpose of this directory is to enable **real-time inference** of the trained and quantized CNN model on FPGA hardware by:

- Managing communication between the host CPU and FPGA
- Loading FPGA overlays and bitstreams
- Invoking hardware-accelerated inference kernels
- Transferring input images and receiving predictions

This code connects the exported ONNX model to actual hardware execution.

---

## System Architecture Context

The full inference system consists of:

- **Host processor:** ARM Cortex-A9
- **Accelerator:** ZtaChip FPGA
- **Model format:** Quantized INT8 ONNX
- **Execution mode:** Batch size = 1 (real-time inference)

The hardware accelerator offloads the convolution-heavy workloads from the CPU, significantly reducing latency.

---

## Functionality Provided

Typical responsibilities of code in this directory include:

- Initializing FPGA overlays
- Configuring accelerator parameters
- Managing memory buffers and data movement
- Sending preprocessed image tensors to the FPGA
- Receiving classification results
- Measuring inference latency and throughput

These components enable consistent benchmarking between CPU-only and FPGA-accelerated execution.

---

## Performance Impact

Using the hardware execution path implemented here, the system achieves:

| Metric       | CPU (ARM Cortex-A9) | FPGA (ZtaChip) |
|--------------|---------------------|---------------|
| Latency      | ~120 ms/frame       | ~25 ms/frame  |
| Throughput   | ~8 FPS              | ~35 FPS       |
| Speedup      | —                   | ~4.8×         |

This demonstrates that FPGA acceleration enables **real-time ASL recognition (>30 FPS)** while maintaining accuracy.

---

## Relationship to Other Directories

- **Model source:** `src/model/`
- **HLS kernels:** `hls/`
- **FPGA overlays:** `overlay/`
- **Trained models:** `models/`
- **Evaluation results:** `figures/`, `report/`

This modular organization supports clean separation between **model design**, **hardware implementation**, and **system evaluation**.

---

## Hardware–Software Co-Design Emphasis

This directory reflects several key AI hardware principles:

- Convolution-heavy workloads benefit from FPGA parallelism
- Quantization reduces memory bandwidth and power consumption
- End-to-end system performance depends on data movement efficiency
- Hardware constraints must be considered early in model design

Rather than treating hardware as an afterthought, the system was designed **end-to-end for deployment**.

---

## Summary

The `src/hardware/` directory implements the **execution backbone** of the project, enabling efficient, low-latency CNN inference on FPGA hardware. Together with the model and HLS components, it completes a full **AI hardware deployment pipeline** suitable for real-time edge AI applications.
