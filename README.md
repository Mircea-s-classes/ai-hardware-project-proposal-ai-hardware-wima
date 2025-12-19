# FPGA-Accelerated Real-Time ASL Alphabet Recognition  
*# FPGA-Accelerated Real-Time ASL Alphabet Recognition  
**AI Hardware Final Project – Hardware/Software Co-Design**

---

## Team Members
- **Maïva Ndjiakou Kaptue**
- **Wil Berling**
- **Daniel Lee**

---

## Project Motivation
Sign language recognition is a critical human–computer interaction problem with strong relevance to **accessibility, assistive technologies, and inclusive design**. Real-time interpretation of hand gestures requires both high classification accuracy and **low, stable inference latency**.

While deep learning models achieve excellent accuracy, most implementations rely on **general-purpose CPUs or GPUs**. CPUs often exhibit **latency jitter** due to operating system scheduling and shared resources, which degrades real-time user experience and limits deployment in embedded systems.

This project explores **FPGA-based acceleration** as a practical solution to:

- Reduce inference latency and variability  
- Improve execution determinism  
- Enable deployment on embedded and low-power platforms  

Our goal is not only to build a functional ASL classifier, but also to design a **complete hardware–aware ML workflow** that goes from dataset and model all the way to a working FPGA overlay, numerical validation, and quantitative benchmarks.

---

## Project Overview

We implement a real-time **American Sign Language (ASL) alphabet recognition system** and evaluate two execution platforms:

1. **PC-based software baseline (CPU-only)**
2. **FPGA-accelerated embedded system using the PYNQ-Z1 board**

A convolutional neural network (CNN) is trained to classify ASL hand gestures from grayscale images. The trained model is **partially offloaded to FPGA hardware** by accelerating the first convolutional block using a **custom Vitis HLS IP core**, while the remaining layers execute on the ARM processor under TensorFlow Lite.

The project includes:

- A full training and evaluation pipeline in Python/TensorFlow  
- ONNX export and weight extraction for hardware  
- Vitis HLS design of a Conv1 accelerator  
- Vivado block design and bitstream generation  
- PYNQ-based runtime integration and benchmarking scripts  
- A LaTeX report documenting the entire flow

---

## System Architecture

### End-to-End Pipeline

1. **Camera frame acquisition** (webcam)  
2. **Preprocessing**: grayscale conversion and resizing to 28×28  
3. **CNN inference**  
4. **ASL letter prediction and display**

### Hardware / Software Partition

- **CPU baseline (PC):**  
  Entire CNN executed on the host CPU (TensorFlow).

- **CPU+FPGA deployment (PYNQ-Z1):**  
  - Conv1 + ReLU + MaxPool implemented as `asl_conv1` IP and executed in programmable logic.  
  - Remaining CNN layers (Conv2 + FCs) implemented as a TFLite “tail” model executing on the ARM cores.  
  - Feature maps are exchanged via DDR using AXI master interfaces.

<p align="center">
  <img src="figures/asl_cnn_fpga_split.png" width="600">
</p>

This partition mirrors typical CNN-on-FPGA strategies: early convolutions are compute-intensive and highly parallelizable, while later layers are kept in software for flexibility.

---

## Dataset and Preprocessing

- **Dataset:** ASL Alphabet Dataset (Kaggle)  
- **Input format:** 28×28 grayscale images  
- **Classes:** 25 static ASL alphabet letters  

Preprocessing steps:

- Normalize pixel intensities to [0, 1]  
- Reshape to `(28, 28, 1)`  
- For live demo: crop hand region from webcam frame, resize to 28×28, and feed into the CNN.

The **exact same preprocessing** is used for the CPU baseline and the PYNQ deployment, ensuring a **fair apples-to-apples comparison**.

---

## Neural Network Model

The CNN is designed for low-resolution grayscale inputs and embedded deployment:

- `Conv2D(32, 3×3)` → ReLU → MaxPool  
- `Conv2D(64, 3×3)` → ReLU → MaxPool  
- `Dense(128)` → ReLU  
- `Dense(25)` → Softmax  

<p align="center">
  <img src="figures/netron_asl_model.png" width="600">
</p>

The model achieves high accuracy while remaining small enough to run comfortably on both CPU and FPGA “tail” inference.

---

## Implementation Details

### Software Baseline (PC)

- Implemented in **Python + TensorFlow/Keras**.  
- Trained and evaluated on the ASL dataset.  
- Provides:
  - Training curves (accuracy vs epochs).  
  - Validation/test accuracy.  
  - Per-inference latency and throughput (FPS) on CPU.  
- Serves as the **golden reference** for both numerical correctness and performance.

<p align="center">
  <img src="figures/Accuracy.png" width="600">
</p>

### HLS Accelerator (`asl_conv1`)

- Written in **C/C++ for Vitis HLS**.  
- Top-level function:  
  `void asl_conv1(float *in, float *out);`  
- Implements:
  - Conv1 with 32 3×3 filters  
  - ReLU activation  
  - 2×2 max pooling  
- Uses trained weights and biases from `weights_init.h`.  
- Exposed as:
  - AXI4-Lite control interface  
  - AXI4 master `m_axi_gmem` for input/output feature maps  

<p align="center">
  <img src="figures/vitis_hls_asl_conv1_screenshot.png" width="700">
</p>

### Vivado Block Design and Overlay

- HLS IP packaged and instantiated inside a **Zynq-7020** block design `asl_system`.  
- Connected to:
  - `processing_system7_0` (Zynq PS)  
  - AXI Interconnect to DDR via S_AXI_HP0  
  - Clock/reset infrastructure (`rst_ps7_0_50M`)  
- Exported as `asl_system.bit` + `asl_system.hwh` overlay for PYNQ.

<p align="center">
  <img src="figures/vivado_bd_asl_system.png" width="600">
</p>

### Synthesis, Implementation, and Resource Utilization

<p align="center">
  <img src="figures/vivado_synthesis_success.png" width="600">
</p>

<p align="center">
  <img src="figures/vivado_implementation_success.png" width="600">
</p>

**Conv1 accelerator footprint on xc7z020:**

| Resource | Used | Available | Utilization |
|---------|-----:|----------:|------------:|
| Slice LUTs | 681 | 53,200 | 1.28% |
| Slice Registers | 4,791 | 106,400 | 4.50% |
| BRAM Tiles | 0 | 140 | 0.00% |
| DSP Slices | 0 | 220 | 0.00% |

The core is **extremely lightweight**, leaving plenty of headroom to accelerate additional layers in future revisions.

---

## Experimental Results and Benchmarks

### 1. CPU Baseline (PC)

**Classification performance**

- Test accuracy: **≈ 98%**  
- Stable training and validation curves with no significant overfitting.

**Latency and jitter**

- Mean latency (batch=1): **83.521 ms**  
- Standard deviation: **29.625 ms**  
- Throughput: **11.97 FPS**  

<p align="center">
  <img src="figures/CPU Latency .png" width="45%">
  <img src="figures/Latency-Distribution.png" width="45%">
</p>

The latency histogram shows **heavy-tailed jitter** due to OS scheduling and shared resources, which is undesirable for real-time interaction.

---

### 2. CPU+FPGA Deployment (PYNQ-Z1)

We evaluate the full CPU+FPGA pipeline on the PYNQ‑Z1:

1. Image is preprocessed to 28×28 on the ARM core.  
2. `asl_conv1` computes Conv1+ReLU+MaxPool on the FPGA.  
3. The resulting \(13×13×32\) feature map is flattened and passed to a TFLite “tail” model (Conv2 + FCs) on the ARM CPU.  
4. The final ASL letter prediction is produced.

#### End-to-End Accuracy

<p align="center">
  <img src="figures/Accuracy_Benchmark.jpg" width="450">
</p>

- **CPU only:** 98.24%  
- **CPU+FPGA:** 98.44%  

Accuracy is effectively unchanged (CPU+FPGA is slightly higher due to test-set randomness), demonstrating that offloading Conv1 to hardware does **not** degrade recognition quality.

#### Conv1 Hardware–Software Numerical Agreement

Using saved feature maps (`feat_sw_conv1.npy` vs `feat_hw_conv1.npy`) we compute:

- Mean-squared error (MSE): **9.9 × 10⁻⁷**  
- Mean absolute error (MAE): **7.9 × 10⁻⁴**  
- Max absolute difference: **4.5 × 10⁻³**

<p align="center">
  <img src="figures/hwsw_error_bar.png" width="450">
</p>

All errors are **well below 10⁻²**, matching expectations for fixed‑point / floating‑point rounding noise and confirming that the HLS implementation is numerically faithful to the reference CNN.

#### Latency and Throughput

<p align="center">
  <img src="figures/Inference_Latency-Benchmark.jpg" width="500">
</p>

Measured over 500 single-sample inferences:

| Metric | CPU only | CPU+FPGA |
|--------|---------:|---------:|
| Mean latency (ms) | 83.81 | 28.18 |
| Std latency (ms)  | 29.11 | 8.58 |
| Throughput (FPS)  | 11.93 | 35.49 |

**Highlights:**

- **≈ 3× lower mean latency** when Conv1 is offloaded to the FPGA.  
- **Latency jitter is reduced by more than 3×**, leading to much smoother response.  
- **Throughput improves from ~12 FPS to ~35 FPS**, comfortably exceeding the ~30 FPS realtime threshold.

Combined with the tiny numerical error and preserved accuracy, these results show a **significant performance win with essentially no quality trade‑off**.

---

## Why This Project Is Exceptional

This project goes far beyond a simple ML model or a one-off FPGA demo:

- Implements a **complete hardware/software co-design pipeline**:
  - From dataset → CNN training → ONNX → HLS → Vivado → PYNQ runtime.  
- Demonstrates **real performance gains**:
  - 3× speedup and reduced jitter, measured with robust benchmarks.  
- Provides **strong validation**:
  - End-to-end accuracy CPU vs CPU+FPGA.  
  - Detailed numerical comparison (MSE/MAE/MAX) of hardware vs software Conv1.  
- Achieves all this with **minimal FPGA resource usage**, leaving room for deeper acceleration.  
- Includes thorough documentation:
  - Full LaTeX report.  
  - Structured code and overlay files.  
  - Clear README and usage instructions.

In short, the project shows how careful hardware-aware ML design can turn a standard CNN into an efficient, **embedded‑ready ASL recognizer** without sacrificing accuracy.

---

## How to Reproduce

### 1. Hardware and Software Requirements

- **Hardware**
  - PYNQ-Z1 board (Zynq‑7020)
  - Micro‑USB cable (power + UART)
  - Ethernet connection to local network
  - Host PC on same network

- **Software**
  - PYNQ image on SD card (with Jupyter support)
  - Python 3.x on host PC (for training / baseline)
  - TensorFlow / Keras on PC
  - NumPy, Matplotlib  
  - Vivado + Vitis HLS (for rebuilding the overlay, if desired)

### 2. Repository Structure

