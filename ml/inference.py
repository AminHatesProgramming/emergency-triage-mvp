from __future__ import annotations

import pickle
import re
from pathlib import Path
from typing import Any

import pandas as pd

from ml.train import add_clinical_features, build_feature_matrix


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "models" / "triage_model_v7.pkl"

HISTORY_LABELS = {
    "htn": "hypertension",
    "diabmelnoc": "diabetes without chronic complications",
    "diabmelwcm": "diabetes with chronic complications",
    "copd": "COPD",
    "asthma": "asthma",
    "chfnonhp": "heart failure",
    "coronathero": "coronary atherosclerosis",
    "chrkidneydisease": "chronic kidney disease",
    "dysrhythmia": "cardiac dysrhythmia",
    "acutemi": "acute myocardial infarction history",
    "acutecvd": "cerebrovascular disease",
    "septicemia": "septicemia history",
    "mooddisorders": "mood disorder",
}


def normalize_chief_complaint(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "", value.lower())
    return f"cc_{cleaned}"


class TriagePredictor:
    def __init__(self, model_path: Path = DEFAULT_MODEL_PATH) -> None:
        self.model_path = model_path
        self.artifact: dict[str, Any] | None = None

    def load(self) -> None:
        if self.artifact is None:
            with self.model_path.open("rb") as f:
                self.artifact = pickle.load(f)

    @property
    def version(self) -> str:
        self.load()
        return str(self.artifact["version"])

    @property
    def metrics(self) -> dict[str, Any]:
        self.load()
        return self.artifact.get("metrics", {})

    def predict(self, patient: dict[str, Any]) -> dict[str, Any]:
        self.load()
        assert self.artifact is not None

        row = {
            "age": patient.get("age"),
            "gender": patient.get("gender", "missing"),
            "arrivalmode": self.normalize_arrival_mode(patient.get("arrivalmode", "Walk-in")),
            "arrivalmonth": patient.get("arrivalmonth", "missing"),
            "arrivalday": patient.get("arrivalday", "missing"),
            "arrivalhour_bin": patient.get("arrivalhour_bin", "missing"),
            "previousdispo": patient.get("previousdispo", "No previous dispo"),
            "triage_vital_hr": patient.get("heart_rate"),
            "triage_vital_sbp": patient.get("systolic_bp"),
            "triage_vital_dbp": patient.get("diastolic_bp"),
            "triage_vital_rr": patient.get("respiratory_rate"),
            "triage_vital_o2sat": patient.get("oxygen_saturation"),
            "triage_vital_temp": patient.get("temperature"),
            "triage_vital_o2_device": self.normalize_o2_device(patient.get("oxygen_device", 0)),
            "n_edvisits": patient.get("previous_ed_visits", 0),
            "n_admissions": patient.get("previous_admissions", 0),
            "n_surgeries": patient.get("previous_surgeries", 0),
            "esi": 3,
        }

        complaint = patient.get("chief_complaint")
        if complaint:
            row[normalize_chief_complaint(str(complaint))] = 1

        history_features = set(
            self.artifact.get("feature_metadata", {}).get("history_features", [])
        )
        for condition in patient.get("history_conditions") or []:
            cleaned = re.sub(r"[^a-z0-9_]+", "", str(condition).lower())
            if cleaned in history_features:
                row[cleaned] = 1

        df = pd.DataFrame([row])
        X, _ = build_feature_matrix(df)
        X = X.reindex(columns=self.artifact["feature_names"], fill_value=0)
        X = X.replace([float("inf"), float("-inf")], pd.NA)
        X_np = self.artifact["scaler"].transform(
            self.artifact["imputer"].transform(X)
        )

        model_probability = 0.0
        for name, weight in self.artifact["weights"].items():
            if weight:
                model_probability += (
                    weight * self.artifact["models"][name].predict_proba(X_np)[0, 1]
                )

        threshold = float(self.artifact["threshold"])
        safety_flags = self.safety_flags(patient)
        safety_override = bool(safety_flags)
        probability = float(model_probability)
        if safety_override:
            probability = max(probability, min(0.99, threshold + 0.08))
        is_critical = probability >= threshold
        completeness, missing_fields, confidence_band = self.data_quality(patient)
        next_best_actions = self.next_best_actions(
            is_critical=is_critical,
            confidence_band=confidence_band,
            safety_flags=safety_flags,
            missing_fields=missing_fields,
        )
        return {
            "model_version": self.artifact["version"],
            "operational_mode": "safety_first_hybrid",
            "model_probability": float(model_probability),
            "critical_probability": float(probability),
            "threshold": threshold,
            "risk_level": "critical" if is_critical else "non_critical",
            "triage_band": (
                "ESI 1-2 priority suggested" if is_critical else "ESI 3-5 standard workflow"
            ),
            "recommended_action": (
                "Immediate clinical review recommended"
                if is_critical
                else "Continue standard triage workflow"
            ),
            "explanation": self.explain(patient, safety_flags=safety_flags),
            "safety_flags": safety_flags,
            "next_best_actions": next_best_actions,
            "safety_override": safety_override,
            "data_completeness": completeness,
            "confidence_band": confidence_band,
            "missing_recommended_fields": missing_fields,
            "disclaimer": "Decision-support only; not a replacement for clinical judgment.",
        }

    @staticmethod
    def normalize_arrival_mode(value: Any) -> str:
        cleaned = re.sub(r"[^a-z0-9]+", "", str(value or "missing").lower())
        return {
            "ambulance": "ambulance",
            "walkin": "Walk-in",
            "wheelchair": "Wheelchair",
            "car": "Car",
            "police": "Police",
            "publictransportation": "Public Transportation",
            "other": "Other",
            "missing": "missing",
        }.get(cleaned, str(value or "missing"))

    @staticmethod
    def normalize_o2_device(value: Any) -> str:
        try:
            return f"{float(value):.1f}"
        except (TypeError, ValueError):
            return "missing"

    @staticmethod
    def explain(patient: dict[str, Any], safety_flags: list[str] | None = None) -> list[str]:
        reasons: list[str] = []
        if safety_flags:
            reasons.extend(safety_flags[:2])
        if patient.get("oxygen_saturation") is not None and patient["oxygen_saturation"] < 94:
            reasons.append("low oxygen saturation")
        if patient.get("systolic_bp") and patient.get("heart_rate"):
            if patient["systolic_bp"] > 0 and patient["heart_rate"] / patient["systolic_bp"] > 1:
                reasons.append("elevated shock index")
        if patient.get("respiratory_rate") is not None and (
            patient["respiratory_rate"] < 12 or patient["respiratory_rate"] > 20
        ):
            reasons.append("abnormal respiratory rate")
        if patient.get("age") is not None and patient["age"] >= 65:
            reasons.append("elderly patient")
        if patient.get("chief_complaint"):
            reasons.append(f"chief complaint: {patient['chief_complaint']}")
        history = patient.get("history_conditions") or []
        if history:
            labels = [HISTORY_LABELS.get(str(item), str(item)) for item in history[:2]]
            reasons.append("known history: " + ", ".join(labels))
        deduped = list(dict.fromkeys(reasons))
        return deduped[:4] or ["no single dominant risk factor identified"]

    @staticmethod
    def safety_flags(patient: dict[str, Any]) -> list[str]:
        flags: list[str] = []
        o2sat = patient.get("oxygen_saturation")
        sbp = patient.get("systolic_bp")
        hr = patient.get("heart_rate")
        rr = patient.get("respiratory_rate")
        temp = patient.get("temperature")
        age = patient.get("age")
        complaint = str(patient.get("chief_complaint") or "").lower()
        history = {str(item).lower() for item in patient.get("history_conditions") or []}

        if o2sat is not None and o2sat < 90:
            flags.append("red flag: oxygen saturation below 90%")
        elif o2sat is not None and o2sat < 94:
            flags.append("warning: oxygen saturation below normal triage range")

        if sbp is not None and sbp < 90:
            flags.append("red flag: systolic blood pressure below 90")
        if rr is not None and (rr < 8 or rr >= 30):
            flags.append("red flag: severely abnormal respiratory rate")
        if hr is not None and (hr < 45 or hr >= 130):
            flags.append("red flag: severely abnormal heart rate")
        if temp is not None and (temp < 35 or temp >= 40):
            flags.append("red flag: extreme body temperature")
        if (
            "chestpain" in complaint
            and age is not None
            and age >= 50
            and {"coronathero", "acutemi", "dysrhythmia"} & history
        ):
            flags.append("red flag: chest pain with high-risk cardiac history")
        return flags[:4]

    @staticmethod
    def next_best_actions(
        is_critical: bool,
        confidence_band: str,
        safety_flags: list[str],
        missing_fields: list[str],
    ) -> list[str]:
        actions: list[str] = []
        if is_critical:
            actions.append("notify senior triage nurse or emergency physician")
            actions.append("repeat vital signs and keep patient in visible monitored area")
        else:
            actions.append("continue standard triage pathway and document model output")
        if safety_flags:
            actions.append("treat safety flags as clinical prompts, not automated diagnosis")
        if confidence_band != "high" and missing_fields:
            actions.append("collect the highest-value missing triage fields before final disposition")
        return actions[:4]

    @staticmethod
    def data_quality(patient: dict[str, Any]) -> tuple[float, list[str], str]:
        recommended = [
            ("chief_complaint", "chief complaint"),
            ("age", "age"),
            ("heart_rate", "heart rate"),
            ("systolic_bp", "systolic blood pressure"),
            ("diastolic_bp", "diastolic blood pressure"),
            ("respiratory_rate", "respiratory rate"),
            ("oxygen_saturation", "oxygen saturation"),
            ("temperature", "temperature"),
        ]
        present = [key for key, _ in recommended if patient.get(key) not in (None, "")]
        missing = [label for key, label in recommended if patient.get(key) in (None, "")]
        completeness = round(len(present) / len(recommended), 2)
        if completeness >= 0.75:
            band = "high"
        elif completeness >= 0.45:
            band = "medium"
        else:
            band = "limited"
        return completeness, missing, band
