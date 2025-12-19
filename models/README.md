# Trained Models and Model Artifacts

This folder contains the trained neural network models and related artifacts used in the **FPGA-Accelerated Real-Time ASL Alphabet Recognition** project. These files represent different stages and formats of the same ASL classification model, used for software inference, hardware deployment, and benchmarking.

## Contents

- **AI-Hardare-SoftwareCode.ipynb**  
  Jupyter Notebook used to train, validate, and export the ASL convolutional neural network.  
  This notebook includes:
  - Dataset loading and preprocessing
  - Model definition and training
  - Evaluation on validation data
  - Export to multiple deployment formats (Keras, TFLite)

- **sign_language_model.h5**  
  Trained Keras model saved in HDF5 format.  
  This file is used for:
  - Software-based inference on the CPU
  - Weight extraction for hardware acceleration
  - Conversion to other formats (e.g., TFLite, ONNX)

- **sign_language_model.keras**  
  Native Keras model format introduced in newer TensorFlow versions.  
  Functionally equivalent to the `.h5` model, this format preserves model structure, weights, and training configuration.

- **sign_language_model.tflite**  
  TensorFlow Lite version of the trained model, optimized for deployment on embedded and resource-constrained platforms.  
  This model is used for:
  - ARM-side inference on the PYNQ-Z1
  - Hardware/software co-execution with FPGA acceleration

## Notes

- All model files correspond to the same CNN architecture described in the project report.
- The TFLite model is used during FPGA deployment, where the first convolutional layer is accelerated in programmable logic and the remaining layers execute on the ARM processor.
- Large intermediate training files and checkpoints are intentionally excluded from version control.


