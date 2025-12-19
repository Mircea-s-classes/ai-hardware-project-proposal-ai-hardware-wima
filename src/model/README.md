# Model Development (`src/model/`)

This directory contains all **machine learning model–related software** used in the project, covering the complete pipeline from dataset preprocessing through CNN training and ONNX export for hardware deployment.

This folder represents the **software ML stage** of the end-to-end AI hardware system.

---

## Purpose

The goal of the model development stage is to design and train a **lightweight convolutional neural network (CNN)** for American Sign Language (ASL) alphabet recognition that:

- Achieves high classification accuracy
- Meets **FPGA resource constraints**
- Is compatible with **INT8 quantization**
- Can be exported to **ONNX** for deployment on the ZtaChip FPGA accelerator

All architectural and training decisions were made with **hardware deployment in mind**, rather than optimizing for software-only performance.

---

## Model Architecture Overview

The trained model is a **compact CNN** designed for real-time inference:

- **Input resolution:** 64 × 64 RGB images  
- **Architecture:**
  - 3 convolutional blocks with ReLU activations
  - Max-pooling layers for spatial reduction
  - Fully connected output layer (29 ASL classes)
- **Design emphasis:**
  - Convolution-dominated workloads (FPGA-friendly)
  - Minimal parameter count
  - Predictable memory access patterns

---

## Training Pipeline

Model training was implemented in **PyTorch** and includes:

- Dataset loading from `data/asl_dataset/`
- Image preprocessing:
  - Resize to 64 × 64
  - Normalization to [0, 1]
  - NCHW tensor layout
- Data augmentation:
  - Rotation
  - Horizontal flipping
  - Brightness variation
- Training/validation split
- Accuracy monitoring and convergence evaluation

The final trained model achieves approximately **90% validation accuracy**.

---

## ONNX Export & Quantization Preparation

This directory also contains scripts used to:

- Export the trained PyTorch model to **ONNX**
- Prepare the model for **INT8 quantization**
- Ensure operator compatibility with FPGA execution

The exported ONNX models are stored in the `models/` directory, including:
- Floating-point ONNX models
- Quantized INT8 models used for hardware acceleration

---

## Relationship to Other Directories

- **Input data:** `data/asl_dataset/`
- **Trained outputs:** `models/`
- **Hardware deployment:** `src/hardware/`, `overlay/`, `hls/`
- **Evaluation & results:** `figures/`, `report/`

This separation enables **clean modular development** and independent reproduction of results.

---

## Hardware-Aware Design Principles

The model was intentionally designed to:

- Fit within FPGA memory and compute limits
- Minimize memory bandwidth requirements
- Support efficient INT8 inference
- Maintain accuracy after quantization

These constraints reflect real-world **AI hardware co-design practices**.

---

## Summary

The `src/model/` directory implements the **software foundation** of the project, bridging raw data and FPGA deployment. It demonstrates how modern CNNs can be structured and trained for **efficient edge AI inference**, rather than purely software-centric benchmarks.
