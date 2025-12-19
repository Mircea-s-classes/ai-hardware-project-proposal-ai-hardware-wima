# FPGA-Accelerated Real-Time ASL Alphabet Recognition  
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
- Reduce inference latency variability  
- Improve execution determinism  
- Enable deployment on embedded and low-power platforms  

---

## Project Overview
This project implements a real-time **American Sign Language (ASL) alphabet recognition system** and evaluates two execution platforms:

1. **PC-based software baseline (CPU-only)**
2. **FPGA-accelerated embedded system using the PYNQ-Z1 board**

A convolutional neural network (CNN) is trained to classify ASL hand gestures from grayscale images. The trained model is **partially offloaded to FPGA hardware** by accelerating the first convolutional block using a **custom HLS-generated IP core**, while the remaining layers execute on the ARM processor.


---

## System Architecture

### End-to-End Pipeline
1. Camera frame acquisition  
2. Image preprocessing (grayscale, resizing to 28×28)  
3. CNN inference  
4. ASL letter prediction  

### Hardware / Software Partition
- **CPU baseline:** Entire CNN executed on the host CPU  
- **FPGA-accelerated path:**
  - Conv1 + ReLU + MaxPool on FPGA programmable logic  
  - Remaining CNN layers on ARM processor (TensorFlow Lite)  

<p align="center">
  <img src="figures/asl_cnn_fpga_split.png" width="600">
</p>

---

## Dataset and Preprocessing
- **Dataset:** ASL Alphabet Dataset (Kaggle)
- **Image format:** 28×28 grayscale
- **Classes:** 25 ASL alphabet letters  

The same preprocessing pipeline is applied for both CPU and FPGA execution to ensure a **fair and meaningful comparison**.

---

## Neural Network Model
The CNN architecture is optimized for low-resolution grayscale input:

- Conv(32) → ReLU → MaxPool  
- Conv(64) → ReLU → MaxPool  
- Dense(128) → ReLU  
- Dense(25) → Softmax  

<p align="center">
  <img src="figures/netron_asl_model.png" width="600">
</p>

---

## Implementation

### PC-Based Software Baseline
- Python + TensorFlow  
- Real-time webcam inference  
- Used for training, debugging, and benchmarking  
- Serves as the reference implementation  

---

### FPGA-Based Implementation (PYNQ-Z1)

#### HLS Accelerator Design
The first convolutional block is implemented as a **custom Vitis HLS IP core** using weights exported from the trained Keras model.

<p align="center">
  <img src="figures/vitis_hls_asl_conv1_screenshot.png" width="700">
</p>

#### Vivado Integration
The HLS IP is integrated into a Zynq block design and synthesized for the PYNQ-Z1 FPGA.

<p align="center">
  <img src="figures/vivado_bd_asl_system.png" width="600">
</p>

#### FPGA Synthesis and Implementation
<p align="center">
  <img src="figures/vivado_synthesis_success.png" width="600">
</p>

<p align="center">
  <img src="figures/vivado_implementation_success.png" width="600">
</p>

---

## Results and Benchmarking

### CPU Baseline Results
- High validation accuracy  
- Mean inference latency ≈ **83.521 ms**  
- Standard deviation ≈ **29.625 ms**  
- Throughput ≈ **11.97 FPS**  
- Observable latency variability (jitter)  

<p align="center">
  <img src="figures/Accuracy.png" width="600">
</p>

<p align="center">
  <img src="figures/CPU Latency .png" width="45%">
  <img src="figures/Latency-Distribution.png" width="45%">
</p>

### FPGA Results (Current Progress)
- Successful FPGA overlay generation (bitstream + .hwh)  
- Functional hardware/software partition verified (Conv1 on FPGA, tail on ARM)  
- Very low FPGA resource utilization for `asl_conv1`:
  - LUTs: 681 / 53,200 (1.28%)  
  - FFs: 4,791 / 106,400 (4.50%)  
  - BRAM: 0 / 140 (0.00%)  
  - DSP: 0 / 220 (0.00%)  

Additional FPGA latency/throughput benchmarks will be added.

---

## HowTo: Use the Software with the Hardware Platform (PYNQ-Z1)
> **This section is required and graded. It explains how to use the software together with the hardware platform.**  
> This README is continuously updated and serves as the **final project report** (motivation + structure + meaningful results).

### Requirements
- PYNQ-Z1 board with a PYNQ image installed  
- Micro-USB cable (power + UART)  
- Ethernet cable (recommended: board ↔ router)  
- Host PC on the same network (Wi-Fi is fine)  
- Serial terminal (MobaXterm on Windows, or `screen/minicom` on Linux)  
- Web browser (Chrome/Edge/Firefox)

---

### Step 1 – Connect and Boot the Board
1. Set boot mode to **SD** (JP4 jumper on SD position)  
2. Insert the microSD card with the PYNQ image  
3. Connect **micro-USB** to the board (PROG-UART) and your PC  
4. Connect **Ethernet** from the board to your router/switch  
5. Power ON the board and wait for the normal boot LED sequence to finish  

---

### Step 2 – Access the Board via Serial
1. On Windows: open **Device Manager** → identify the board COM port (example: `COM9`)  
2. Open **MobaXterm** → **Session** → **Serial**  
3. Set:
   - **Port:** your COM port (ex: `COM9`)  
   - **Baud rate:** `115200`  

You should now see the PYNQ Linux terminal.

---

### Step 3 – Get the Board IP Address
In the serial terminal, run:
```bash
ifconfig -a
```

### Step 4 – Access the PYNQ Jupyter Notebook

1. On your host PC, open a browser and go to:

   `https://<BOARD_IP>`

2. Login (default PYNQ credentials):

   - **username:** `xilinx`  
   - **password:** `xilinx`

> If your browser shows a security warning (self-signed certificate), click **Advanced → Proceed**.
--

### Step 5 – Load the FPGA Overlay
In a Jupyter notebook cell:
```python
from pynq import Overlay
overlay = Overlay("asl_system_wrapper.bit")
overlay.download()
```

---

### Step 6 – Run ASL Inference
1. Capture a webcam frame  
2. Convert to grayscale  
3. Resize to 28×28  
4. Normalize pixel values  
5. Run inference and display predicted ASL letter  

---

## Repository Structure
```text
figures/        # Figures used in README and report
models/         # Trained CNN and ONNX models
hls/            # Vitis HLS source code
vivado/         # Vivado block design and bitstreams
pynq/           # Jupyter notebooks and overlays
benchmarks/     # CPU/FPGA benchmarking scripts
report/         # LaTeX report
README.md
```

---

## Limitations
- Only the first convolution layer is accelerated on FPGA  


---

## Future Work 
- Power and determinism analysis  

---

## Demo Video
A demo video will be added demonstrating real-time ASL recognition on the PYNQ-Z1.

---

## Conclusion
This project demonstrates a complete **AI hardware co-design workflow**, from CNN training to FPGA deployment, highlighting the benefits and challenges of FPGA acceleration for real-time embedded AI.
