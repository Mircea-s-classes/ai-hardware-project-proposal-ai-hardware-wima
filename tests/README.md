# Validation & Correctness Tests

This directory contains tests used to validate numerical correctness
and robustness of the inference pipeline.

## Tests
- `numerical_correctness.py`: Compares CPU and accelerated inference outputs
  within floating-point tolerances

These tests ensure hardware acceleration does not compromise inference accuracy.
