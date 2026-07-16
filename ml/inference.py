from __future__ import annotations

import pickle
import re
from pathlib import Path
from typing import Any

import pandas as pd

from ml.train import add_clinical_features, build_feature_matrix


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "models" / "triage_model_v7.pkl"
SAFETY_RULE_VERSION = "2026.07.2"

SPARSE_OPERATING_THRESHOLDS = {
    "complaint_hr_o2": 0.16415970027446747,
    "complaint_age_hr_o2": 0.1881568878889084,
}

SEVERITY_RANK = {"none": 0, "urgent": 1, "immediate": 2}

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


def normalize_chief_complaint(value: str, age: float | None = None) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "", value.lower())
    if cleaned == "fall" and age is not None and age >= 65:
        return "cc_fall>65"
    aliases = {
        "fever": "cc_fever-9weeksto74years",
        "headache": "cc_headache-newonsetornewsymptoms",
        "headachenewonsetornewsymptoms": "cc_headache-newonsetornewsymptoms",
    }
    if cleaned in aliases:
        return aliases[cleaned]
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

    def operating_profile(self, patient: dict[str, Any]) -> tuple[str, float]:
        self.load()
        assert self.artifact is not None
        default_threshold = float(self.artifact["threshold"])
        has_complaint = bool(str(patient.get("chief_complaint") or "").strip())
        has_hr = patient.get("heart_rate") is not None
        has_o2 = patient.get("oxygen_saturation") is not None
        other_vitals_absent = all(
            patient.get(field) is None
            for field in ["systolic_bp", "diastolic_bp", "respiratory_rate", "temperature"]
        )
        if has_complaint and has_hr and has_o2 and other_vitals_absent:
            if patient.get("age") is None:
                return "validated_sparse_3", SPARSE_OPERATING_THRESHOLDS["complaint_hr_o2"]
            return "validated_sparse_4", SPARSE_OPERATING_THRESHOLDS["complaint_age_hr_o2"]
        return "full_v7_default", default_threshold

    def transformed_features(self, patient: dict[str, Any]) -> Any:
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
            row[normalize_chief_complaint(str(complaint), patient.get("age"))] = 1

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
        return X_np

    def predict(self, patient: dict[str, Any]) -> dict[str, Any]:
        self.load()
        assert self.artifact is not None
        X_np = self.transformed_features(patient)

        model_probability = 0.0
        for name, weight in self.artifact["weights"].items():
            if weight:
                model_probability += (
                    weight * self.artifact["models"][name].predict_proba(X_np)[0, 1]
                )

        operating_profile, threshold = self.operating_profile(patient)
        safety = self.safety_assessment(patient)
        safety_flags = safety["flags"]
        safety_severity = safety["severity"]
        safety_override = safety_severity != "none"
        model_is_critical = float(model_probability) >= threshold
        is_critical = model_is_critical or safety_severity == "immediate"
        if is_critical:
            risk_level = "critical"
        elif safety_severity == "urgent":
            risk_level = "urgent"
        else:
            risk_level = "non_critical"
        if model_is_critical and safety_override:
            assessment_basis = "model_and_safety_rule"
        elif model_is_critical:
            assessment_basis = "model"
        elif safety_override:
            assessment_basis = "safety_rule"
        else:
            assessment_basis = "model"
        completeness, missing_fields, confidence_band = self.data_quality(patient)
        next_best_actions = self.next_best_actions(
            risk_level=risk_level,
            safety_severity=safety_severity,
            confidence_band=confidence_band,
            safety_flags=safety_flags,
            measurement_warnings=safety["measurement_warnings"],
            missing_fields=missing_fields,
        )
        return {
            "model_version": self.artifact["version"],
            "operational_mode": "safety_first_hybrid",
            "operating_profile": operating_profile,
            "model_probability": float(model_probability),
            # Retained for API compatibility. This is the unmodified model estimate;
            # clinical urgency is represented separately by risk_level and safety_severity.
            "critical_probability": float(model_probability),
            "threshold": threshold,
            "risk_level": risk_level,
            "triage_band": {
                "critical": "priority_1_immediate_review",
                "urgent": "priority_2_rapid_review",
                "non_critical": "standard_triage_review",
            }[risk_level],
            "recommended_action": {
                "critical": "Immediate clinical review recommended",
                "urgent": "Rapid clinical review recommended",
                "non_critical": "Continue standard triage workflow",
            }[risk_level],
            "explanation": self.explain(patient, safety_flags=safety_flags),
            "safety_flags": safety_flags,
            "next_best_actions": next_best_actions,
            "safety_override": safety_override,
            "safety_severity": safety_severity,
            "assessment_basis": assessment_basis,
            "safety_rule_version": SAFETY_RULE_VERSION,
            "measurement_warnings": safety["measurement_warnings"],
            "out_of_distribution": safety["out_of_distribution"],
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
    def safety_assessment(patient: dict[str, Any]) -> dict[str, Any]:
        flags: list[str] = []
        measurement_warnings: list[str] = []
        severity = "none"
        o2sat = patient.get("oxygen_saturation")
        sbp = patient.get("systolic_bp")
        dbp = patient.get("diastolic_bp")
        hr = patient.get("heart_rate")
        rr = patient.get("respiratory_rate")
        temp = patient.get("temperature")
        age = patient.get("age")
        complaint = str(patient.get("chief_complaint") or "").lower()
        history = {str(item).lower() for item in patient.get("history_conditions") or []}
        oxygen_device = patient.get("oxygen_device")
        safety_points = 0
        safety_domains = 0

        def add_flag(message: str, level: str) -> None:
            nonlocal severity
            flags.append(message)
            if SEVERITY_RANK[level] > SEVERITY_RANK[severity]:
                severity = level

        def add_measurement_warning(field: str) -> None:
            measurement_warnings.append(
                f"verify measurement: {field} is outside the expected triage input range"
            )

        def add_points(points: int) -> None:
            nonlocal safety_points, safety_domains
            if points > 0:
                safety_points += points
                safety_domains += 1

        if o2sat is not None and o2sat < 90:
            add_flag("immediate: oxygen saturation below 90%", "immediate")
        elif o2sat is not None and o2sat < 94:
            add_flag("urgent: oxygen saturation below normal triage range", "urgent")
        if o2sat is not None:
            add_points(3 if o2sat <= 91 else 2 if o2sat <= 93 else 1 if o2sat <= 95 else 0)
        try:
            if oxygen_device is not None and float(oxygen_device) > 0:
                safety_points += 2
        except (TypeError, ValueError):
            pass
        if o2sat is not None and o2sat < 50:
            add_measurement_warning("oxygen saturation")

        is_adult_or_unknown = age is None or age >= 16
        if sbp is not None and is_adult_or_unknown and sbp <= 90:
            add_flag("immediate: adult systolic blood pressure at or below 90", "immediate")
        elif sbp is not None and is_adult_or_unknown and 90 < sbp <= 100:
            add_flag("urgent: adult systolic blood pressure between 91 and 100", "urgent")
        elif sbp is not None and is_adult_or_unknown and sbp >= 220:
            add_flag("urgent: adult systolic blood pressure at or above 220", "urgent")
        if sbp is not None and is_adult_or_unknown:
            add_points(3 if sbp <= 90 or sbp >= 220 else 2 if sbp <= 100 else 1 if sbp <= 110 else 0)
        if sbp is not None and (sbp < 40 or sbp > 260):
            add_measurement_warning("systolic blood pressure")
        if dbp is not None and (dbp < 20 or dbp > 160):
            add_measurement_warning("diastolic blood pressure")
        if sbp is not None and dbp is not None and (dbp >= sbp or sbp - dbp < 10):
            add_measurement_warning("systolic/diastolic blood pressure relationship")

        if sbp is not None and age is not None and age < 16:
            if age < 1:
                pediatric_hypotension_threshold = 70
            elif age <= 10:
                pediatric_hypotension_threshold = 70 + 2 * age
            else:
                pediatric_hypotension_threshold = 90
            if sbp < pediatric_hypotension_threshold:
                add_flag("immediate: pediatric systolic blood pressure below age-adjusted threshold", "immediate")
                add_points(3)

        if rr is not None and is_adult_or_unknown and (rr <= 8 or rr >= 30):
            add_flag("immediate: severely abnormal adult respiratory rate", "immediate")
        elif rr is not None and is_adult_or_unknown and (9 <= rr <= 11 or 21 <= rr <= 29):
            add_flag("urgent: adult respiratory rate outside the stable range", "urgent")
        if rr is not None and is_adult_or_unknown:
            add_points(3 if rr <= 8 or rr >= 25 else 2 if rr >= 21 else 1 if rr <= 11 else 0)
        if rr is not None and (rr < 3 or rr > 70):
            add_measurement_warning("respiratory rate")

        if hr is not None:
            if is_adult_or_unknown:
                if hr >= 150:
                    add_flag("immediate: adult heart rate at or above 150/min", "immediate")
                elif hr >= 130:
                    add_flag("urgent: adult heart rate between 130 and 149/min", "urgent")
                if hr < 40:
                    add_flag("immediate: adult heart rate below 40/min", "immediate")
                elif hr <= 50:
                    add_flag("urgent: adult heart rate between 40 and 50/min", "urgent")
                elif 111 <= hr < 130:
                    add_flag("urgent: adult heart rate between 111 and 129/min", "urgent")
                add_points(3 if hr <= 40 or hr >= 131 else 2 if hr >= 111 else 1 if hr <= 50 or hr >= 91 else 0)
            elif age is not None and age < 1:
                if hr >= 220:
                    add_flag("immediate: infant heart rate at or above 220/min", "immediate")
                elif hr >= 150:
                    add_flag("urgent: infant heart rate above age-adjusted review threshold", "urgent")
                if hr < 80:
                    add_flag("immediate: markedly low infant heart rate", "immediate")
                add_points(3 if hr >= 160 or hr < 80 else 2 if hr >= 150 else 0)
            else:
                if hr >= 180:
                    add_flag("immediate: child heart rate at or above 180/min", "immediate")
                else:
                    assert age is not None
                    if age < 3:
                        moderate_hr, high_hr = 140, 150
                    elif age < 5:
                        moderate_hr, high_hr = 130, 140
                    elif age < 6:
                        moderate_hr, high_hr = 120, 130
                    elif age < 8:
                        moderate_hr, high_hr = 110, 120
                    elif age < 12:
                        moderate_hr, high_hr = 105, 115
                    else:
                        moderate_hr, high_hr = 111, 131
                    if hr >= moderate_hr:
                        add_flag("urgent: child heart rate above age-adjusted review threshold", "urgent")
                    add_points(3 if hr >= high_hr else 2 if hr >= moderate_hr else 0)
                if hr < 60:
                    add_flag("immediate: markedly low child heart rate", "immediate")
                    add_points(3)
            if hr < 20 or hr > 250:
                add_measurement_warning("heart rate")

        if rr is not None and age is not None and age < 16:
            if age < 1:
                moderate_rr, high_rr, immediate_rr = 50, 60, 70
            elif age < 3:
                moderate_rr, high_rr, immediate_rr = 40, 50, 60
            elif age < 5:
                moderate_rr, high_rr, immediate_rr = 35, 40, 60
            elif age < 6:
                moderate_rr, high_rr, immediate_rr = 24, 29, 50
            elif age < 8:
                moderate_rr, high_rr, immediate_rr = 24, 27, 50
            elif age < 12:
                moderate_rr, high_rr, immediate_rr = 22, 25, 45
            else:
                moderate_rr, high_rr, immediate_rr = 21, 25, 40
            if rr >= immediate_rr or rr <= 8:
                add_flag("immediate: severely abnormal child respiratory rate", "immediate")
            elif rr >= moderate_rr:
                add_flag("urgent: child respiratory rate above age-adjusted review threshold", "urgent")
            add_points(3 if rr >= high_rr or rr <= 8 else 2 if rr >= moderate_rr else 0)

        if temp is not None and age is not None and age < 0.25 and temp >= 38:
            add_flag("immediate: fever in an infant younger than 3 months", "immediate")
        elif temp is not None and age is not None and age < 0.5 and temp >= 39:
            add_flag("urgent: high fever in an infant aged 3 to 6 months", "urgent")
        if temp is not None and (temp <= 35 or temp >= 40):
            add_flag("immediate: extreme body temperature", "immediate")
        elif temp is not None and (temp < 36 or temp >= 39.1):
            add_flag("urgent: body temperature outside the stable range", "urgent")
        if temp is not None:
            add_points(3 if temp <= 35 else 2 if temp >= 39.1 else 1 if temp < 36 or temp > 38 else 0)
        if temp is not None and (temp < 30 or temp > 43):
            add_measurement_warning("body temperature")

        if is_adult_or_unknown and hr is not None and sbp is not None and sbp > 0:
            shock_index = hr / sbp
            if shock_index >= 1.2:
                add_flag("immediate: markedly elevated shock index", "immediate")
            elif shock_index >= 1.0:
                add_flag("urgent: elevated shock index", "urgent")

        if is_adult_or_unknown and safety_domains >= 2:
            if safety_points >= 7:
                add_flag("immediate: combined adult vital-sign score is high", "immediate")
            elif safety_points >= 5:
                add_flag("urgent: combined adult vital-sign score requires rapid review", "urgent")
        elif not is_adult_or_unknown and safety_domains >= 2 and safety_points >= 6:
            add_flag("immediate: multiple age-adjusted pediatric vital signs are abnormal", "immediate")
        if (
            "chestpain" in complaint
            and age is not None
            and age >= 50
            and {"coronathero", "acutemi", "dysrhythmia"} & history
        ):
            add_flag("immediate: chest pain with high-risk cardiac history", "immediate")

        return {
            "severity": severity,
            "flags": list(dict.fromkeys(flags))[:5],
            "measurement_warnings": list(dict.fromkeys(measurement_warnings))[:3],
            "out_of_distribution": bool(measurement_warnings),
        }

    @staticmethod
    def safety_flags(patient: dict[str, Any]) -> list[str]:
        return TriagePredictor.safety_assessment(patient)["flags"]

    @staticmethod
    def next_best_actions(
        risk_level: str,
        safety_severity: str,
        confidence_band: str,
        safety_flags: list[str],
        measurement_warnings: list[str],
        missing_fields: list[str],
    ) -> list[str]:
        actions: list[str] = []
        if risk_level == "critical":
            actions.append("notify senior triage nurse or emergency physician")
            actions.append("repeat vital signs and keep patient in visible monitored area")
        elif risk_level == "urgent":
            actions.append("request rapid review by the responsible triage clinician")
            actions.append("repeat the abnormal vital sign without delaying clinical review")
        else:
            actions.append("continue standard triage pathway and document model output")
        if measurement_warnings:
            actions.append("verify the outlying measurement and sensor placement immediately")
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
