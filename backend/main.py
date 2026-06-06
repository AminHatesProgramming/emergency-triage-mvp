from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.schemas import PatientInput, PredictionOutput
from ml.inference import TriagePredictor

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"

app = FastAPI(
    title="Emergency Triage Decision Support API",
    version="0.1.0",
    description="MVP API for an AI-assisted emergency triage decision-support project.",
)
predictor = TriagePredictor()

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/model-info")
def model_info() -> dict:
    metrics = predictor.metrics
    return {
        "version": predictor.version,
        "selected_predictor": metrics.get("selected_predictor"),
        "test_metrics": metrics.get("test_metrics"),
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput) -> dict:
    return predictor.predict(patient.model_dump())
