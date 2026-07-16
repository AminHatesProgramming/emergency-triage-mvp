import csv
import os
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
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
from ml.inference import SAFETY_RULE_VERSION, SPARSE_OPERATING_THRESHOLDS, TriagePredictor

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
    title="Emdadyar Decision Support API",
    version="1.0.0",
    description="Final MVP API for Emdadyar emergency assessment decision support.",
)

raw_allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").strip()
allowed_origins = (
    ["*"]
    if raw_allowed_origins == "*"
    else [origin.strip() for origin in raw_allowed_origins.split(",") if origin.strip()]
)
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


@app.get("/manifest.webmanifest")
def manifest() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "manifest.webmanifest")


@app.get("/sw.js")
def service_worker() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "sw.js")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "emdadyar-webapp",
        "model_version": predictor.version,
    }


@app.get("/model-info")
def model_info() -> dict:
    metrics = predictor.metrics
    return {
        "product_name": "Emdadyar",
        "version": predictor.version,
        "selected_predictor": metrics.get("selected_predictor"),
        "test_metrics": metrics.get("test_metrics"),
        "operating_points": metrics.get("operating_points", {}),
        "target_definition": metrics.get("target_definition"),
        "safety_layer": {
            "version": SAFETY_RULE_VERSION,
            "mode": "age-aware deterministic escalation with combined-vital review",
            "model_probability_is_modified": False,
            "adult_age_definition": ">=16 years",
            "adult_tachycardia": {
                "urgent_bpm": "130-149",
                "immediate_bpm": ">=150",
            },
            "pediatric_thresholds_are_age_adjusted": True,
            "combined_vital_sign_escalation": True,
            "outlier_measurements_require_repeat_check": True,
        },
        "validated_sparse_operating_points": {
            "complaint_hr_o2": {
                "threshold": SPARSE_OPERATING_THRESHOLDS["complaint_hr_o2"],
                "test_auc": 0.8158535508343744,
                "test_recall": 0.941085868309588,
                "test_fpr": 0.5900828569593423,
            },
            "complaint_age_hr_o2": {
                "threshold": SPARSE_OPERATING_THRESHOLDS["complaint_age_hr_o2"],
                "test_auc": 0.8355945883084874,
                "test_recall": 0.9245579218625041,
                "test_fpr": 0.5177468045474982,
            },
            "core_vitals_low_threshold_rejected_for_excessive_fpr": True,
        },
        "decision_support_only": True,
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput) -> dict:
    payload = patient.model_dump()
    immediate_signals = (
        "heart_rate",
        "systolic_bp",
        "diastolic_bp",
        "respiratory_rate",
        "oxygen_saturation",
        "temperature",
    )
    has_chief_complaint = bool((payload.get("chief_complaint") or "").strip())
    has_vital_sign = any(payload.get(field) is not None for field in immediate_signals)
    if not has_chief_complaint and not has_vital_sign:
        raise HTTPException(
            status_code=422,
            detail="At least one chief complaint or vital sign is required for an initial assessment.",
        )
    return predictor.predict(payload)


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
