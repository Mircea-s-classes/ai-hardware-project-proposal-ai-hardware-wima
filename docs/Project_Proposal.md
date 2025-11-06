# University of Virginia
## Department of Electrical and Computer Engineering

**Course:** ECE 4332 / ECE 6332 — AI Hardware Design and Implementation  
**Semester:** Fall 2025  
**Proposal Deadline:** November 5, 2025 — 11:59 PM  
**Submission:** Upload to Canvas (PDF) and to GitHub (`/docs` folder)

---

# AI Hardware Project Proposal Template

## 1. Project Title : FPGA-Accelerated Sign Language Recognition Using the Ztachip ​

Name of the Team:WIMA

List of students in the team
1. Maiva Ndjiakou Kaptue
2. Wil Berling

Provide a clear and concise title for your project. 

## 2. Platform Selection

**Chosen Platform: Ztachip**

**Justification:**
- Ztachip is an open-source RISC-V–based FPGA accelerator optimized for CNN inference.
- Provides Python/C++ APIs suitable for real-time vision workloads such as gesture or sign recognition.
- Lightweight and deployable on low-cost FPGA boards — ideal for a month student project.
- Simpler integration compared to NVDLA or VTA, which require heavier toolchains.
- Strong documentation and active community examples support rapid prototyping.


## 3. Problem Definition
The project aims to design and implement a **real-time American Sign Language (ASL) alphabet recognition system** using the **Ztachip FPGA accelerator**. The system must maintain low latency, high accuracy, and operate efficiently on limited hardware resources.

Sign language recognition is computationally intensive. A CPU alone struggles to achieve real-time performance. Ztachip's FPGA acceleration improves throughput by exploiting parallel computation, making it suitable for assistive communication devices.

## 4. Technical Objectives
1. Train a CNN achieving **≥95% accuracy** on a public ASL alphabet dataset.
2. Convert the trained model to ONNX and compile it using the Ztachip toolchain.
3. Achieve **real-time inference of ≥30 FPS** on FPGA hardware.
4. Demonstrate **≥5× reduction** in inference latency compared to CPU.
5. Integrate and test a live camera pipeline on the FPGA platform.


## 5. Methodology
**Hardware Setup:** Ztachip-supported FPGA development board.
- **Software Tools:** PyTorch/TensorFlow, ONNX, Ztachip compiler, Python runtime.
- **Model Architecture:** Lightweight quantized CNN (INT8) optimized for FPGA.
- **Workflow:** Train → ONNX export → Ztachip compile → deploy → integrate camera.
- **Validation:** Measure accuracy, FPS, and compare CPU vs FPGA latency.
<img width="1900" height="1118" alt="better_project_diagram" src="https://github.com/user-attachments/assets/483167b7-1842-4007-be1e-10955957fe7e" />


## 6. Expected Deliverables
- FPGA-accelerated ASL recognition system
- GitHub repository containing full code and documentation
- Performance benchmarking report (CPU vs FPGA)
- Video demonstration of the real-time system
- Final presentation and written technical report


## 7. Team Responsibilities
List each member’s main role.

| Name | Role | Responsibilities |
|------|------|------------------|
| Maiva | Team Lead | Maiva Ndjiakou	Team Lead	Project coordination, dataset preparation, model training|
| Maiva & Wil | Hardware | FPGA setup, Ztachip integration, compiler workflow |
| Maiva | Software |ONNX export, camera interface development |
| Wil| Evaluation | Testing, benchmarking, latency measurements |

## 8. Timeline and Milestones
Provide expected milestones:

| Week | Milestone | Deliverable |
|------|------------|-------------|
| 2 | Proposal | PDF + GitHub submission |
| 4 | Midterm presentation | Slides, preliminary results |
| 6 | Integration & testing | Working prototype |
| Dec. 18 | Final presentation | Report, demo, GitHub archive |

## 9. Resources Required
FPGA development board (PYNQ) compatible with Ztachip
- ASL alphabet dataset
- Development environment with PyTorch/TensorFlow
- Ztachip toolchain and SDK
- USB camera for real-time testing
- Jupyter Notebook environment


## 10. References
**Research Papers:**
1. Chen et al., “Deep Learning Acceleration on FPGAs: A Review,” IEEE TPDS.
2. Molchanov et al., “Hand Gesture Recognition with Deep Learning for Real-Time Applications.”
3. Zhang et al., “TVM: End-to-End Optimization for Deep Learning on Hardware Accelerators.”

**GitHub Repositories:**
- Ztachip (chosen platform): https://github.com/ztachip/ztachip
- ASL Classification Dataset & Model: https://github.com/ardamavi/Sign-Language-Digits-Dataset
- ONNX Model Deployment Examples: https://github.com/onnx/models

