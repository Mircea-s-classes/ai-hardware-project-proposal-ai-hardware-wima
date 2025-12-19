# FPGA-Accelerated Real-Time ASL Alphabet Recognition  
**AI Hardware Final Project – Hardware/Software Co-Design**

---

## Project Overview

This project implements a **real-time American Sign Language (ASL) alphabet recognition system** using **FPGA-based hardware acceleration**. The system combines modern deep learning techniques with embedded hardware optimization to demonstrate how **AI inference performance can be significantly improved through hardware–software co-design**.

A convolutional neural network (CNN)–based classifier is trained in software, exported to ONNX, quantized to INT8 precision, and deployed on a **PYNQ-Z2 FPGA** using the **ZtaChip AI acceleration overlay**. The final system processes live camera input and performs low-latency inference suitable for real-time interaction.

The project emphasizes **system-level optimization**, not just model accuracy, aligning directly with core AI Hardware course concepts such as:
- Data movement and memory bandwidth
- Parallelism and hardware acceleration
- Precision–performance tradeoffs
- End-to-end deployment pipelines

---

## Motivation and Problem Statement

Real-time ASL recognition presents several challenges:

- CNN-based vision models are **computationally intensive**
- CPU-only execution results in **high inference latency**
- Embedded systems require **low power consumption**
- Real-time performance demands **high throughput and low latency**

This project addresses these challenges by accelerating inference on an FPGA, leveraging:
- Fine-grained parallelism in convolution operations
- Reduced-precision arithmetic (INT8 quantization)
- Hardware-aware model design

The central goal is to demonstrate that **embedded FPGA platforms can achieve real-time AI inference without sacrificing accuracy**.

---

## Hardware Platform

### PYNQ-Z2 FPGA Board
- Xilinx Zynq-7020 SoC
- Dual-core ARM Cortex-A9 (Processing System)
- Programmable Logic (FPGA fabric) for acceleration
- Python-based control via the PYNQ framework

### ZtaChip Accelerator
- AI acceleration overlay deployed on FPGA fabric
- Optimized for CNN inference workloads
- Supports INT8-quantized ONNX models
- Enables significant latency reduction compared to CPU execution

---

## Software Stack

- **PyTorch** – Model training and validation  
- **ONNX** – Framework-independent model representation  
- **INT8 Quantization** – Reduced precision for performance and memory efficiency  
- **PYNQ** – Python-based FPGA control  
- **ZtaChip SDK** – Accelerator compilation and execution  
- **Jupyter Notebook** – Interactive development and testing  

---

## Dataset

- **Kaggle ASL Alphabet Dataset**
- ~87,000 labeled RGB images
- One directory per letter (`a/` through `z/`)
- Images preprocessed to:
  - 64×64 resolution
  - Normalized pixel values
  - NCHW tensor format

Due to GitHub size limitations, the full dataset is not included directly. The repository documents the expected structure and usage.

---

## Model Architecture

- Lightweight CNN designed with hardware constraints in mind
- Three convolutional blocks with ReLU activation
- Max-pooling for spatial reduction
- Fully connected output layer (29 classes)
- Data augmentation for robustness:
  - Rotation
  - Flipping
  - Brightness variation

**Validation accuracy:** ~90%  
**Accuracy drop after INT8 quantization:** < 2%

---

## End-to-End System Pipeline

1. Dataset acquisition and preprocessing  
2. CNN model training in PyTorch  
3. Export trained model to ONNX  
4. Apply INT8 quantization  
5. Compile model for ZtaChip accelerator  
6. Deploy accelerator overlay to FPGA  
7. Capture live camera input  
8. Run real-time inference on FPGA  
9. Display predicted ASL letter  
10. Benchmark CPU vs FPGA performance  

---

## Performance Results

| Metric | CPU (ARM Cortex-A9) | FPGA (ZtaChip) |
|------|---------------------|---------------|
| Latency | ~120 ms/frame | ~25 ms/frame |
| Throughput | ~8 FPS | ~35 FPS |
| Speedup | — | ~4.8× |

These results demonstrate that FPGA acceleration enables **real-time performance (>30 FPS)** while maintaining high accuracy.

---

## Repository Structure Guide

This repository is organized to reflect a **clean separation of concerns** between data, software, hardware, and documentation.

ai-hardware-project/
├── data/
│   └── asl_dataset/
│       ├── a/
│       ├── b/
│       ├── ...
│       ├── z/
│       └── README.md
│
├── src/
│   ├── model/
│   │   ├── README.md
│   │   └── CNN training & ONNX export code
│   │
│   ├── hardware/
│   │   └── PYNQ + ZtaChip control code
│   │
│   └── vivado/
│
├── models/
│   └── trained weights, ONNX models, quantized models
│
├── hls/
│   └── HLS accelerator code
│
├── overlay/
│   └── FPGA bitstreams and ZtaChip overlays
│
├── figures/
│   └── plots, diagrams, benchmark figures
│
├── presentations/
│   ├── AI-Hardware-MidTerm-Presentation.pdf
│   └── AI-Hardware-Final-Presentation.pdf
│
├── report/
│   ├── AI_hardware.pdf
│   └── README.md
│
└── README.md


---

## `src/model/` – Model Development Explained

The `src/model/` directory contains all **machine learning model–related logic**, including:

- CNN architecture definitions
- Training and validation code
- ONNX export scripts
- Quantization preparation

This folder represents the **software ML stage** of the pipeline.  
Trained outputs produced here are stored in the `models/` directory and later deployed to hardware.

The model is intentionally designed to:
- Fit FPGA resource constraints
- Be compatible with INT8 quantization
- Support ONNX-based deployment workflows

---

## Hardware–Software Co-Design Emphasis

This project demonstrates several key AI hardware principles:

- **Convolution-dominated workloads** benefit from FPGA parallelism
- **Quantization** is critical for memory and bandwidth efficiency
- **Performance gains** come from system-level optimization
- **Model design must consider hardware constraints early**

Rather than treating hardware as an afterthought, the system was designed end-to-end with deployment in mind.

---

## Reproducibility Notes

- All tests were run using batch size = 1 to reflect real-time inference
- CPU and FPGA evaluations used the same model and input resolution
- Dataset structure and preprocessing steps are fully documented
- Repository organization is designed to support independent replication

---

## Conclusion

This project demonstrates a complete, real-world AI hardware deployment pipeline—from dataset to real-time inference—on an embedded FPGA platform. The results validate that **hardware acceleration is essential for real-time AI**, and that modern deep learning models can be successfully adapted to **resource-constrained hardware** through careful design and optimization.

---

## License

This project is released under the MIT License for academic use.
