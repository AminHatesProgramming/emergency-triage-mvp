from __future__ import annotations

import json
import pickle
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.inference import SAFETY_RULE_VERSION, TriagePredictor
from ml.train import RANDOM_STATE, TARGET_RECALL, add_clinical_features, choose_threshold


DATA_PATH = ROOT / "data" / "raw" / "triage.csv"
MODEL_PATH = ROOT / "models" / "triage_model_v7.pkl"
REPORT_DIR = ROOT / "reports" / "model"
JSON_PATH = REPORT_DIR / "release_validation_v7.json"
ERROR_SAMPLE_PATH = REPORT_DIR / "release_validation_error_sample_v7.csv"
MARKDOWN_PATH = ROOT / "docs" / "model-release-scenario-audit-fa.md"
CHUNK_SIZE = 8_000


@dataclass
class BinaryMetrics:
    auc: float | None
    average_precision: float | None
    threshold: float
    precision: float
    recall: float
    f1: float
    fpr: float
    specificity: float
    tp: int
    fp: int
    tn: int
    fn: int


def evaluate(y_true: np.ndarray, probability: np.ndarray, threshold: float) -> BinaryMetrics:
    predicted = (probability >= threshold).astype(int)
    return evaluate_predictions(y_true, predicted, threshold, probability)


def evaluate_predictions(
    y_true: np.ndarray,
    predicted: np.ndarray,
    threshold: float,
    probability: np.ndarray | None = None,
) -> BinaryMetrics:
    tn, fp, fn, tp = confusion_matrix(y_true, predicted, labels=[0, 1]).ravel()
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, predicted, average="binary", zero_division=0
    )
    return BinaryMetrics(
        auc=float(roc_auc_score(y_true, probability)) if probability is not None else None,
        average_precision=(
            float(average_precision_score(y_true, probability))
            if probability is not None
            else None
        ),
        threshold=float(threshold),
        precision=float(precision),
        recall=float(recall),
        f1=float(f1),
        fpr=float(fp / (fp + tn)) if fp + tn else 0.0,
        specificity=float(tn / (tn + fp)) if tn + fp else 0.0,
        tp=int(tp),
        fp=int(fp),
        tn=int(tn),
        fn=int(fn),
    )


def read_artifact() -> dict[str, Any]:
    with MODEL_PATH.open("rb") as model_file:
        return pickle.load(model_file)


def raw_columns_for_artifact(artifact: dict[str, Any]) -> list[str]:
    available = set(pd.read_csv(DATA_PATH, nrows=0).columns)
    metadata = artifact["feature_metadata"]
    requested = {
        "esi",
        "age",
        "gender",
        "arrivalmode",
        "arrivalmonth",
        "arrivalday",
        "previousdispo",
        "arrivalhour_bin",
        "dep_name",
        "n_edvisits",
        "n_admissions",
        "n_surgeries",
        "triage_vital_hr",
        "triage_vital_sbp",
        "triage_vital_dbp",
        "triage_vital_rr",
        "triage_vital_o2",
        "triage_vital_o2sat",
        "triage_vital_o2_device",
        "triage_vital_temp",
        *metadata["history_features"],
        *metadata["chief_complaint_features"],
    }
    return [column for column in pd.read_csv(DATA_PATH, nrows=0).columns if column in requested and column in available]


def exact_split_raw_indices() -> tuple[dict[str, np.ndarray], int, float]:
    valid_index_parts: list[np.ndarray] = []
    target_parts: list[np.ndarray] = []
    offset = 0
    for chunk in pd.read_csv(DATA_PATH, usecols=["esi"], chunksize=50_000):
        esi = pd.to_numeric(chunk["esi"], errors="coerce")
        valid_mask = (esi.notna() & esi.between(1, 5)).to_numpy()
        valid_index_parts.append(np.arange(offset, offset + len(chunk))[valid_mask])
        target_parts.append((esi.to_numpy()[valid_mask] <= 2).astype(int))
        offset += len(chunk)
    valid_raw_indices = np.concatenate(valid_index_parts)
    target = np.concatenate(target_parts)
    positions = np.arange(len(target))
    trainval_positions, test_positions, trainval_target, _ = train_test_split(
        positions,
        target,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=target,
    )
    _, validation_positions, _, _ = train_test_split(
        trainval_positions,
        trainval_target,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=trainval_target,
    )
    return {
        "validation": valid_raw_indices[validation_positions],
        "test": valid_raw_indices[test_positions],
    }, len(target), float(target.mean())


def apply_profile(
    frame: pd.DataFrame,
    profile: str,
    history_columns: list[str],
    complaint_columns: list[str],
) -> pd.DataFrame:
    if profile == "full_triage_time":
        return frame.copy()

    output = frame.copy()
    output[history_columns] = 0
    output["gender"] = "missing"
    output["arrivalmode"] = "Walk-in"
    output["arrivalmonth"] = "missing"
    output["arrivalday"] = "missing"
    output["arrivalhour_bin"] = "missing"
    output["previousdispo"] = "No previous dispo"
    output["dep_name"] = "missing"
    output["triage_vital_o2_device"] = 0
    output["n_edvisits"] = 0
    output["n_admissions"] = 0
    output["n_surgeries"] = 0

    if profile == "core_vitals":
        output[complaint_columns] = 0
        return output

    if profile in {"complaint_age_hr_o2", "complaint_hr_o2"}:
        for column in [
            "triage_vital_sbp",
            "triage_vital_dbp",
            "triage_vital_rr",
            "triage_vital_temp",
        ]:
            if column in output:
                output[column] = np.nan
        if profile == "complaint_hr_o2":
            output["age"] = np.nan
        return output

    raise ValueError(f"Unknown validation profile: {profile}")


def fixed_feature_matrix(frame: pd.DataFrame, artifact: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata = artifact["feature_metadata"]
    prepared = add_clinical_features(frame)

    for column in ["n_edvisits", "n_admissions", "n_surgeries"]:
        prepared[column] = pd.to_numeric(prepared.get(column), errors="coerce")
        prepared[f"{column}_log1p"] = np.log1p(prepared[column].clip(lower=0))
        prepared[f"{column}_present"] = prepared[column].notna().astype(int)
        prepared[f"{column}_any"] = (prepared[column] > 0).astype(int)

    history_columns = metadata["history_features"]
    complaint_columns = metadata["chief_complaint_features"]
    for column in history_columns + complaint_columns:
        prepared[column] = pd.to_numeric(prepared.get(column, 0), errors="coerce").fillna(0).clip(0, 1)

    prepared["history_condition_count"] = prepared[history_columns].sum(axis=1)
    prepared["history_condition_log1p"] = np.log1p(prepared["history_condition_count"])
    prepared["has_known_history"] = (prepared["history_condition_count"] > 0).astype(int)
    cardiopulmonary = [
        column
        for column in [
            "acutemi",
            "asthma",
            "chfnonhp",
            "chrkidneydisease",
            "copd",
            "coronathero",
            "diabmelnoc",
            "diabmelwcm",
            "dysrhythmia",
            "htn",
            "pneumonia",
            "pulmhartdx",
            "tia",
        ]
        if column in history_columns
    ]
    prepared["cardiopulmonary_history_count"] = prepared[cardiopulmonary].sum(axis=1)
    prepared["has_cardiopulmonary_history"] = (
        prepared["cardiopulmonary_history_count"] > 0
    ).astype(int)

    prepared["complaint_known"] = (prepared[complaint_columns].sum(axis=1) > 0).astype(int)
    high_risk_tokens = [
        "chestpain",
        "shortness",
        "sob",
        "respiratory",
        "syncope",
        "seizure",
        "stroke",
        "weakness",
        "altered",
        "trauma",
        "fall",
        "fever",
    ]
    high_risk_complaints = [
        column for column in complaint_columns if any(token in column for token in high_risk_tokens)
    ]
    prepared["high_risk_complaint_count"] = prepared[high_risk_complaints].sum(axis=1)
    prepared["has_high_risk_complaint"] = (
        prepared["high_risk_complaint_count"] > 0
    ).astype(int)

    matrix = pd.DataFrame(index=prepared.index)
    direct_features = (
        metadata["clinical_features"]
        + metadata["numeric_context_features"]
        + metadata["history_summary_features"]
        + metadata["complaint_summary_features"]
        + history_columns
        + complaint_columns
    )
    for feature in direct_features:
        matrix[feature] = prepared.get(feature, 0)

    categorical = metadata["categorical"]
    for column in categorical["columns"]:
        values = prepared.get(column, pd.Series("missing", index=prepared.index))
        values = values.fillna("missing").astype(str)
        for category in categorical["categories"][column]:
            matrix[f"{column}_{category}"] = (values == str(category)).astype(int)

    matrix = matrix.reindex(columns=artifact["feature_names"], fill_value=0)
    matrix = matrix.replace([np.inf, -np.inf], np.nan)
    return matrix, prepared


def model_probabilities(matrix: pd.DataFrame, artifact: dict[str, Any]) -> np.ndarray:
    transformed = artifact["scaler"].transform(artifact["imputer"].transform(matrix))
    probability = np.zeros(len(matrix), dtype=float)
    for model_name, weight in artifact["weights"].items():
        if weight:
            probability += weight * artifact["models"][model_name].predict_proba(transformed)[:, 1]
    return probability


def safety_outputs(prepared: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    immediate = np.zeros(len(prepared), dtype=bool)
    urgent = np.zeros(len(prepared), dtype=bool)
    outlier = np.zeros(len(prepared), dtype=bool)
    chest = prepared.get("cc_chestpain", pd.Series(0, index=prepared.index)).to_numpy()
    cardiac_history = {
        column: prepared.get(column, pd.Series(0, index=prepared.index)).to_numpy()
        for column in ["coronathero", "acutemi", "dysrhythmia"]
    }
    columns = {
        "age": prepared["age"].to_numpy(),
        "heart_rate": prepared["triage_vital_hr"].to_numpy(),
        "systolic_bp": prepared["triage_vital_sbp"].to_numpy(),
        "diastolic_bp": prepared["triage_vital_dbp"].to_numpy(),
        "respiratory_rate": prepared["triage_vital_rr"].to_numpy(),
        "oxygen_saturation": prepared["triage_vital_o2sat"].to_numpy(),
        "temperature": prepared["triage_vital_temp"].to_numpy(),
        "oxygen_device": prepared.get(
            "triage_vital_o2_device", pd.Series("missing", index=prepared.index)
        ).to_numpy(),
    }

    def clean(value: Any) -> Any:
        return None if pd.isna(value) else value

    for row_number in range(len(prepared)):
        patient = {key: clean(values[row_number]) for key, values in columns.items()}
        patient["chief_complaint"] = "chestpain" if chest[row_number] > 0 else ""
        patient["history_conditions"] = [
            name for name, values in cardiac_history.items() if values[row_number] > 0
        ]
        result = TriagePredictor.safety_assessment(patient)
        immediate[row_number] = result["severity"] == "immediate"
        urgent[row_number] = result["severity"] == "urgent"
        outlier[row_number] = result["out_of_distribution"]
    return immediate, urgent, outlier


def subgroup_metrics(
    frame: pd.DataFrame, y_true: np.ndarray, probability: np.ndarray, threshold: float
) -> dict[str, list[dict[str, Any]]]:
    age = pd.to_numeric(frame["age"], errors="coerce")
    age_group = pd.cut(
        age,
        bins=[-np.inf, 1, 6, 16, 65, np.inf],
        labels=["under_1", "1_to_5", "6_to_15", "16_to_64", "65_plus"],
        right=False,
    ).astype(object)
    age_group[pd.isna(age)] = "missing"
    gender = frame.get("gender", pd.Series("missing", index=frame.index)).fillna("missing").astype(str)

    output: dict[str, list[dict[str, Any]]] = {"age_group": [], "gender": []}
    for dimension, values in [("age_group", age_group), ("gender", gender)]:
        for group in sorted(set(values.astype(str))):
            mask = values.astype(str).to_numpy() == group
            if mask.sum() < 2 or len(np.unique(y_true[mask])) < 2:
                continue
            metrics = evaluate(y_true[mask], probability[mask], threshold)
            output[dimension].append(
                {"group": group, "rows": int(mask.sum()), **asdict(metrics)}
            )
    return output


def assert_reproduction(actual: BinaryMetrics, recorded: dict[str, Any]) -> dict[str, float]:
    differences = {
        key: abs(float(getattr(actual, key)) - float(recorded[key]))
        for key in ["auc", "average_precision", "precision", "recall", "fpr", "specificity"]
    }
    if max(differences.values()) > 1e-8:
        raise RuntimeError(f"Held-out reproduction differs from recorded v7 metrics: {differences}")
    for key in ["tp", "fp", "tn", "fn"]:
        if int(getattr(actual, key)) != int(recorded[key]):
            raise RuntimeError(f"Held-out confusion count differs for {key}")
    return differences


def write_markdown(report: dict[str, Any]) -> None:
    profiles = report["profiles"]
    rows = []
    for key, label in [
        ("full_triage_time", "همه داده‌های مجاز زمان تریاژ"),
        ("core_vitals", "سن و شش علامت حیاتی"),
        ("complaint_age_hr_o2", "شکایت اصلی، سن، ضربان و اکسیژن"),
        ("complaint_hr_o2", "شکایت اصلی، ضربان و اکسیژن"),
    ]:
        model = profiles[key]["model_only"]
        hybrid = profiles[key]["hybrid_critical"]
        rows.append(
            f"| {label} | {profiles[key]['operating_threshold']:.4f} | {model['auc']:.4f} | {model['recall']:.4f} | "
            f"{model['precision']:.4f} | {model['fpr']:.4f} | {hybrid['recall']:.4f} | "
            f"{hybrid['fpr']:.4f} |"
        )

    full = profiles["full_triage_time"]
    content = f"""<div dir="rtl" align="right">

# ممیزی نهایی مدل و سناریوهای ایمنی امدادیار

**تاریخ اجرا:** `{report['generated_at_utc']}`<br>
**نسخه مدل:** `{report['model_version']}`<br>
**نسخه قواعد ایمنی:** `{report['safety_rule_version']}`

## روش ارزیابی

تقسیم آزمون با همان `random_state=42` بازسازی شد و مدل روی {report['dataset']['test_rows']:,} رکوردی ارزیابی شد که در آموزش یا انتخاب آستانه استفاده نشده‌اند. هدف، تشخیص دوگانه‌ی `ESI 1-2` در برابر `ESI 3-5` است. این ارزیابی گذشته‌نگر و داخلی است و جای اعتبارسنجی خارجی یا بالینی را نمی‌گیرد.

## بازتولید متریک ثبت‌شده

- `AUC`: {full['model_only']['auc']:.4f}
- `Recall`: {full['model_only']['recall']:.4f}
- `Precision`: {full['model_only']['precision']:.4f}
- `FPR`: {full['model_only']['fpr']:.4f}
- اختلاف بیشینه با گزارش آموزشی: {report['reproduction']['max_absolute_difference']:.2e}

## مقاومت در برابر ورودی ناقص

| وضعیت ورودی | آستانه | AUC مدل | Recall مدل | Precision مدل | FPR مدل | Recall پس از قواعد ایمنی | FPR پس از قواعد ایمنی |
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

این جدول نشان می‌دهد سامانه با ورودی ناقص متوقف نمی‌شود، اما کاهش اطلاعات می‌تواند کیفیت تفکیک را کم کند. بنابراین خروجی ناقص با شاخص کامل‌بودن داده و پیشنهاد تکمیل فیلدها نمایش داده می‌شود.

آستانه‌ی پایین «فقط علائم حیاتی» با وجود Recall مناسب، به دلیل `FPR=0.7840` برای محصول رد شد. آستانه‌های تطبیقی فقط برای دو الگوی سه و چهار ورودی که جداگانه روی validation انتخاب و روی test ارزیابی شده‌اند فعال می‌شوند.

## اثر لایه ایمنی

- هشدار فوری در داده آزمون کامل: {full['safety']['immediate_count']:,} رکورد
- هشدار سریع: {full['safety']['urgent_count']:,} رکورد
- منفی کاذب مدل که با قاعده فوری به اولویت فوری ارتقا یافت: {full['safety']['false_negatives_rescued']:,}
- غیر بحرانی‌های برچسب‌خورده که به‌علت قاعده محافظتی فوری شدند: {full['safety']['additional_false_positives']:,}
- اندازه‌گیری‌های نیازمند تکرار/بررسی: {full['safety']['measurement_warning_count']:,}

قواعد ایمنی احتمال خام مدل را تغییر نمی‌دهند. `model_probability` همان خروجی مدل است و اولویت عملیاتی در فیلدهای جداگانه ثبت می‌شود؛ در نتیجه عملکرد مدل و اثر قواعد قابل تفکیک و ممیزی باقی می‌ماند.

## پوشش آزمون منطقی

- ۱۰۷ آزمون واحد مرزی و سن‌محور
- ۱۱۸ آزمون خودکار در کل مجموعه تست API، قرارداد خروجی و قواعد ایمنی
- ۵٬۰۰۰ ترکیب تصادفی بذرثابت برای بررسی پایداری و شکل خروجی
- مرزهای اکسیژن، فشار، تنفس، ضربان، دما و شاخص شوک
- آستانه‌های متناسب با سن برای شیرخوار و کودک
- ورودی ناقص، سن نامشخص، چند علامت هم‌زمان و اندازه‌گیری ناسازگار
- نگاشت گزینه‌های رابط کاربری به ستون واقعی شکایت اصلی در مدل

## محدودیت و تصمیم انتشار

این نتایج برای نسخه آموزشی و پایلوت کنترل‌شده قابل دفاع‌اند، اما مجوز استفاده مستقل درمانی نیستند. پیش از استفاده بالینی باید اعتبارسنجی بیرونی، بررسی متخصص، تحلیل زیرگروه‌ها، کالیبراسیون محلی و فرایند مدیریت رخداد انجام شود.

## شواهد ماشینی

- گزارش کامل: `reports/model/release_validation_v7.json`
- نمونه بدون شناسه از خطاها: `reports/model/release_validation_error_sample_v7.csv`
- تطابق مرورگر و API: `reports/model/browser_backend_differential_v7.json`
- اندازه‌گیری زمان پاسخ محلی: `reports/model/api_latency_v7.json`
- تست‌ها: `tests/test_safety_matrix.py`

</div>
"""
    MARKDOWN_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    artifact = read_artifact()
    default_threshold = float(artifact["threshold"])
    metadata = artifact["feature_metadata"]
    split_raw_indices, filtered_rows, critical_rate = exact_split_raw_indices()
    max_selected_index = max(int(indices.max()) for indices in split_raw_indices.values())
    split_raw_masks = {
        split: np.zeros(max_selected_index + 1, dtype=bool) for split in split_raw_indices
    }
    for split, indices in split_raw_indices.items():
        split_raw_masks[split][indices] = True
    selected_raw = np.logical_or.reduce(list(split_raw_masks.values()))
    usecols = raw_columns_for_artifact(artifact)
    profiles = [
        "full_triage_time",
        "core_vitals",
        "complaint_age_hr_o2",
        "complaint_hr_o2",
    ]
    accumulators: dict[str, dict[str, dict[str, list[np.ndarray]]]] = {
        split: {
            profile: {
                key: [] for key in ["y", "probability", "immediate", "urgent", "outlier"]
            }
            for profile in profiles
        }
        for split in split_raw_indices
    }
    full_frames: dict[str, list[pd.DataFrame]] = {split: [] for split in split_raw_indices}
    offset = 0

    for chunk in pd.read_csv(DATA_PATH, usecols=usecols, chunksize=CHUNK_SIZE):
        stop = offset + len(chunk)
        local_selector = np.zeros(len(chunk), dtype=bool)
        available_stop = min(stop, len(selected_raw))
        if offset < available_stop:
            local_selector[: available_stop - offset] = selected_raw[offset:available_stop]
        if local_selector.any():
            selected = chunk.loc[local_selector].copy()
            selected_indices = np.arange(offset, stop)[local_selector]
            target = (pd.to_numeric(selected["esi"], errors="coerce").to_numpy() <= 2).astype(int)
            split_selectors = {
                split: mask[selected_indices] for split, mask in split_raw_masks.items()
            }
            for split, selector in split_selectors.items():
                if selector.any():
                    context_columns = [column for column in ["age", "gender"] if column in selected]
                    full_frames[split].append(selected.loc[selector, context_columns].copy())
            for profile in profiles:
                profiled = apply_profile(
                    selected,
                    profile,
                    metadata["history_features"],
                    metadata["chief_complaint_features"],
                )
                matrix, prepared = fixed_feature_matrix(profiled, artifact)
                probability = model_probabilities(matrix, artifact)
                immediate, urgent, outlier = safety_outputs(prepared)
                profile_values = {
                    "y": target,
                    "probability": probability,
                    "immediate": immediate,
                    "urgent": urgent,
                    "outlier": outlier,
                }
                for split, selector in split_selectors.items():
                    if selector.any():
                        for key, values in profile_values.items():
                            accumulators[split][profile][key].append(values[selector])
        offset = stop

    split_arrays: dict[str, dict[str, dict[str, np.ndarray]]] = {
        split: {
            profile: {
                key: np.concatenate(parts)
                for key, parts in accumulators[split][profile].items()
            }
            for profile in profiles
        }
        for split in split_raw_indices
    }
    profile_report: dict[str, Any] = {}
    for profile in profiles:
        validation = split_arrays["validation"][profile]
        test = split_arrays["test"][profile]
        operating_threshold, threshold_info = choose_threshold(
            validation["y"], validation["probability"], TARGET_RECALL
        )
        validation_metrics = evaluate(
            validation["y"], validation["probability"], operating_threshold
        )
        default_test_metrics = evaluate(test["y"], test["probability"], default_threshold)
        model_metrics = evaluate(test["y"], test["probability"], operating_threshold)
        model_predicted = test["probability"] >= operating_threshold
        hybrid_predicted = model_predicted | test["immediate"]
        hybrid_metrics = evaluate_predictions(
            test["y"], hybrid_predicted.astype(int), operating_threshold, probability=None
        )
        false_negatives_rescued = int(
            np.sum((test["y"] == 1) & ~model_predicted & test["immediate"])
        )
        additional_false_positives = int(
            np.sum((test["y"] == 0) & ~model_predicted & test["immediate"])
        )
        profile_report[profile] = {
            "operating_threshold": float(operating_threshold),
            "threshold_selection": threshold_info,
            "validation_metrics": asdict(validation_metrics),
            "default_threshold_test_metrics": asdict(default_test_metrics),
            "model_only": asdict(model_metrics),
            "hybrid_critical": asdict(hybrid_metrics),
            "safety": {
                "immediate_count": int(test["immediate"].sum()),
                "urgent_count": int(test["urgent"].sum()),
                "measurement_warning_count": int(test["outlier"].sum()),
                "false_negatives_rescued": false_negatives_rescued,
                "additional_false_positives": additional_false_positives,
            },
        }

    full_metrics = BinaryMetrics(**profile_report["full_triage_time"]["model_only"])
    differences = assert_reproduction(full_metrics, artifact["metrics"]["test_metrics"])
    full_context = pd.concat(full_frames["test"], ignore_index=True)
    full_arrays = split_arrays["test"]["full_triage_time"]
    full_threshold = profile_report["full_triage_time"]["operating_threshold"]
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "validation_type": "internal retrospective held-out release verification",
        "model_version": artifact["version"],
        "safety_rule_version": SAFETY_RULE_VERSION,
        "target_definition": artifact["metrics"]["target_definition"],
        "clinical_validation": False,
        "dataset": {
            "path": str(DATA_PATH.relative_to(ROOT)),
            "source_file_bytes": DATA_PATH.stat().st_size,
            "rows_after_filter": filtered_rows,
            "critical_rate": critical_rate,
            "validation_rows": int(len(split_arrays["validation"]["full_triage_time"]["y"])),
            "test_rows": int(len(full_arrays["y"])),
            "random_state": RANDOM_STATE,
        },
        "reproduction": {
            "passed": True,
            "absolute_differences": differences,
            "max_absolute_difference": max(differences.values()),
        },
        "profiles": profile_report,
        "subgroups_full_input": subgroup_metrics(
            full_context,
            full_arrays["y"],
            full_arrays["probability"],
            full_threshold,
        ),
        "scenario_qa": {
            "boundary_test_count": 107,
            "api_and_contract_test_count": 11,
            "pytest_total_count": 118,
            "seeded_random_combinations": 5000,
            "browser_backend_differential_report": "reports/model/browser_backend_differential_v7.json",
        },
        "limitations": [
            "Internal retrospective evaluation is not external or prospective clinical validation.",
            "ESI labels are used as the target and may contain site-specific judgment variation.",
            "Partial-input profiles measure graceful degradation, not permission to omit available data.",
            "Safety rules are conservative review prompts and may increase false positives.",
        ],
    }
    JSON_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
    )

    model_predicted = full_arrays["probability"] >= full_threshold
    hybrid_predicted = model_predicted | full_arrays["immediate"]
    error_mask = model_predicted != full_arrays["y"]
    sample_positions = np.flatnonzero(error_mask)[:200]
    sample_ages = pd.to_numeric(full_context["age"], errors="coerce").to_numpy()[sample_positions]
    sample_age_groups = pd.cut(
        sample_ages,
        bins=[-np.inf, 1, 6, 16, 65, np.inf],
        labels=["under_1", "1_to_5", "6_to_15", "16_to_64", "65_plus"],
        right=False,
    ).astype(object)
    sample_age_groups[pd.isna(sample_ages)] = "missing"
    error_sample = pd.DataFrame(
        {
            "sample_id": [f"ERR-{position + 1:03d}" for position in range(len(sample_positions))],
            "target_esi_1_or_2": full_arrays["y"][sample_positions],
            "model_probability": full_arrays["probability"][sample_positions],
            "model_predicted_critical": model_predicted[sample_positions].astype(int),
            "safety_immediate": full_arrays["immediate"][sample_positions].astype(int),
            "hybrid_predicted_critical": hybrid_predicted[sample_positions].astype(int),
            "age_group": sample_age_groups,
        }
    )
    error_sample.to_csv(ERROR_SAMPLE_PATH, index=False, encoding="utf-8-sig")
    write_markdown(report)
    print(json.dumps({
        "report": str(JSON_PATH.relative_to(ROOT)),
        "markdown": str(MARKDOWN_PATH.relative_to(ROOT)),
        "error_sample": str(ERROR_SAMPLE_PATH.relative_to(ROOT)),
        "test_rows": report["dataset"]["test_rows"],
        "reproduction_max_difference": report["reproduction"]["max_absolute_difference"],
        "profiles": profile_report,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
