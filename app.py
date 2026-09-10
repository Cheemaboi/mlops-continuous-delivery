"""Small, versioned inference service for the CD demonstration."""

from pathlib import Path
import os

from flask import Flask, jsonify, request


APP_ROOT = Path(__file__).resolve().parent
DEFAULT_VERSION = (APP_ROOT / "VERSION").read_text(encoding="utf-8").strip()
APPLICATION_VERSION = os.getenv("APPLICATION_VERSION", DEFAULT_VERSION)
MODEL_VERSION = os.getenv("MODEL_VERSION", "model-6")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({"service": "mlops-continuous-delivery", "status": "running"})


@app.get("/health")
def health():
    return jsonify(
        {
            "application_version": APPLICATION_VERSION,
            "model_version": MODEL_VERSION,
            "git_commit": GIT_COMMIT,
            "status": "healthy",
        }
    )


@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    try:
        value = float(data["value"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "value must be a number"}), 400

    return jsonify(
        {
            "input": value,
            "prediction": value * 2,
            "model_version": MODEL_VERSION,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
