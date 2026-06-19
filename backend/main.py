import csv
import os
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.schemas import (
    PatientInput,
    PredictionOutput,
    StakeholderFeedbackInput,
    StakeholderFeedbackOutput,
)
from ml.inference import TriagePredictor

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
DOCS_DIR = ROOT / "docs"
FEEDBACK_DIR = ROOT / "data" / "feedback"
FEEDBACK_CSV = FEEDBACK_DIR / "stakeholder_feedback.csv"
FEEDBACK_FIELDS = [
    "recorded_at",
    "stakeholder_type",
    "understandability",
    "ui_clarity",
    "disclaimer_clarity",
    "comment",
]

app = FastAPI(
    title="Emergency Triage Decision Support API",
    version="0.1.0",
    description="MVP API for an AI-assisted emergency triage decision-support project.",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)
predictor = TriagePredictor()

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

if DOCS_DIR.exists():
    app.mount("/docs", StaticFiles(directory=DOCS_DIR), name="docs")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "emergency-triage-webapp",
        "model_version": predictor.version,
    }


@app.get("/model-info")
def model_info() -> dict:
    metrics = predictor.metrics
    return {
        "version": predictor.version,
        "selected_predictor": metrics.get("selected_predictor"),
        "test_metrics": metrics.get("test_metrics"),
        "operating_points": metrics.get("operating_points", {}),
        "target_definition": metrics.get("target_definition"),
        "decision_support_only": True,
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput) -> dict:
    return predictor.predict(patient.model_dump())


def ensure_feedback_file() -> None:
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    if not FEEDBACK_CSV.exists():
        with FEEDBACK_CSV.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=FEEDBACK_FIELDS)
            writer.writeheader()


def feedback_count() -> int:
    ensure_feedback_file()
    with FEEDBACK_CSV.open("r", newline="", encoding="utf-8-sig") as f:
        return max(sum(1 for _ in f) - 1, 0)


@app.post("/feedback", response_model=StakeholderFeedbackOutput)
def submit_feedback(feedback: StakeholderFeedbackInput) -> dict:
    ensure_feedback_file()
    row = feedback.model_dump()
    row["recorded_at"] = datetime.now(timezone.utc).isoformat()
    with FEEDBACK_CSV.open("a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FEEDBACK_FIELDS)
        writer.writerow({key: row.get(key, "") for key in FEEDBACK_FIELDS})
    return {
        "status": "stored",
        "stored_count": feedback_count(),
        "export_path": "/feedback/export",
    }


@app.get("/feedback-summary")
def feedback_summary() -> dict:
    return {
        "stored_count": feedback_count(),
        "target_count": 5,
        "export_path": "/feedback/export",
    }


@app.get("/feedback/export")
def export_feedback() -> FileResponse:
    ensure_feedback_file()
    return FileResponse(
        FEEDBACK_CSV,
        media_type="text/csv; charset=utf-8",
        filename="triage-stakeholder-feedback.csv",
    )
