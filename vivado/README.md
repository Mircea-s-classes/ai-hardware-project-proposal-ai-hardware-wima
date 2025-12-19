# Vivado Design

This folder contains the **Vivado hardware design files** used to generate the FPGA overlay for the **FPGA-accelerated ASL recognition system** targeting the **PYNQ-Z1 (Zynq-7020)** board.

The design integrates a custom **HLS-generated Conv1 accelerator** with the Zynq processing system through AXI interconnects and provides the hardware platform used by the Python inference pipeline on PYNQ.

## Contents

- **asl_system.bd**  
  Vivado block design describing the complete hardware system, including the Zynq Processing System, AXI interconnect, and the custom `asl_conv1` accelerator IP.

- **asl_system_wrapper.tcl**  
  TCL script that can be used to recreate the Vivado project and block design automatically. This enables reproducibility without requiring the full project directory.

- **asl_system_wrapper.dcp**  
  Synthesized design checkpoint corresponding to the top-level wrapper. This file captures the post-synthesis state of the design.

- **asl_system.bit**  
  Generated FPGA bitstream used to configure the programmable logic on the PYNQ-Z1 board.

- **asl_system.hwh**  
  Hardware handoff file required by PYNQ to expose the FPGA overlay and its AXI interfaces to Python.

## Notes

- Generated Vivado directories and cache files (e.g., `.Xil/`, `.runs/`, `.cache/`) are **intentionally excluded** from version control to keep the repository lightweight and portable.
- The design can be regenerated using the provided TCL script together with the HLS sources in the `hls/` directory.
- This overlay accelerates the **first convolutional block (Conv1 + ReLU + MaxPool)** of the ASL CNN, while the remaining network layers execute on the ARM processor.


