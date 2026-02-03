from fastapi import FastAPI
import torch
import numpy as np

app = FastAPI(title="ASL Inference API")

# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = "model/inference/model.pt"
INPUT_SHAPE = (1, 1, 64, 64)

model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/predict")
def predict():
    """
    Dummy inference endpoint.
    In real deployment, input would come from camera or frontend.
    """
    with torch.no_grad():
        dummy_input = torch.randn(INPUT_SHAPE)
        output = model(dummy_input)
        prediction = int(torch.argmax(output, dim=1).item())

    return {
        "prediction": prediction,
        "status": "success"
    }

