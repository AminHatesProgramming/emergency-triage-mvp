"""Train the emergency triage decision-support model.

The script intentionally uses only information that can plausibly be available
at triage time: age, arrival mode, first vital signs, and chief complaint flags.
That keeps the model easier to defend in a project-management presentation and
reduces the risk of leakage from later hospital events.
"""

from __future__ import annotations

import argparse
import json
import pickle
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, RobustScaler

try:
    import shap
except ImportError:  # pragma: no cover - optional reporting dependency
    shap = None

try:
    import xgboost as xgb
except ImportError:  # pragma: no cover - optional model dependency
    xgb = None


warnings.filterwarnings("ignore")

RANDOM_STATE = 42
TARGET_RECALL = 0.92
MIN_CC_PREVALENCE = 0.005

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "triage.csv"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports" / "model"
MODEL_PATH = MODEL_DIR / "triage_model_v5.pkl"
METRICS_PATH = REPORT_DIR / "metrics_v5.json"


def training_usecols(path: Path) -> list[str]:
    columns = pd.read_csv(path, nrows=0).columns.tolist()
    required = {
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
        "triage_vital_hr",
        "triage_vital_sbp",
        "triage_vital_dbp",
        "triage_vital_rr",
        "triage_vital_o2",
        "triage_vital_o2sat",
        "triage_vital_o2_device",
        "triage_vital_temp",
        "pulse_last",
        "resp_last",
        "spo2_last",
        "sbp_last",
        "dbp_last",
        "temp_last",
    }
    selected = [col for col in columns if col in required or col.startswith("cc_")]
    return selected


@dataclass
class SplitMetrics:
    auc: float
    average_precision: float
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


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize source column variants used by different dataset exports."""
    df = df.copy()
    aliases = {
        "triage_vital_o2sat": ["triage_vital_o2", "spo2_last"],
        "triage_vital_rr": ["triage_vital_rr", "resp_last"],
        "triage_vital_hr": ["triage_vital_hr", "pulse_last"],
        "triage_vital_sbp": ["triage_vital_sbp", "sbp_last"],
        "triage_vital_dbp": ["triage_vital_dbp", "dbp_last"],
        "triage_vital_temp": ["triage_vital_temp", "temp_last"],
    }

    for canonical, candidates in aliases.items():
        if canonical not in df.columns:
            for candidate in candidates:
                if candidate in df.columns:
                    df[canonical] = df[candidate]
                    break
        if canonical not in df.columns:
            df[canonical] = np.nan

    return df


def add_clinical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    df = df.copy()

    numeric_cols = [
        "age",
        "triage_vital_hr",
        "triage_vital_sbp",
        "triage_vital_dbp",
        "triage_vital_rr",
        "triage_vital_o2sat",
        "triage_vital_temp",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df.get(col, np.nan), errors="coerce")

    sbp = df["triage_vital_sbp"].replace(0, np.nan)
    dbp = df["triage_vital_dbp"].replace(0, np.nan)
    rr = df["triage_vital_rr"].replace(0, np.nan)

    df["shock_index"] = df["triage_vital_hr"] / sbp
    df["map"] = (df["triage_vital_sbp"] + 2 * dbp) / 3
    df["pulse_pressure"] = df["triage_vital_sbp"] - df["triage_vital_dbp"]
    df["hr_rr_ratio"] = df["triage_vital_hr"] / rr

    df["hr_abnormal"] = (
        (df["triage_vital_hr"] < 60) | (df["triage_vital_hr"] > 100)
    ).astype(int)
    df["sbp_abnormal"] = (
        (df["triage_vital_sbp"] < 90) | (df["triage_vital_sbp"] > 180)
    ).astype(int)
    df["rr_abnormal"] = (
        (df["triage_vital_rr"] < 12) | (df["triage_vital_rr"] > 20)
    ).astype(int)
    df["o2_abnormal"] = (df["triage_vital_o2sat"] < 94).astype(int)
    df["temp_abnormal"] = (
        (df["triage_vital_temp"] < 36) | (df["triage_vital_temp"] > 38.5)
    ).astype(int)
    df["map_abnormal"] = ((df["map"] < 70) | (df["map"] > 110)).astype(int)
    df["shock_index_abnormal"] = (df["shock_index"] > 1.0).astype(int)
    df["vital_severity_score"] = (
        df["hr_abnormal"]
        + df["sbp_abnormal"]
        + df["rr_abnormal"]
        + df["o2_abnormal"]
        + df["temp_abnormal"]
        + df["map_abnormal"]
        + df["shock_index_abnormal"]
    )

    df["age_group"] = pd.cut(
        df["age"], bins=[0, 2, 12, 18, 65, 200], labels=[0, 1, 2, 3, 4]
    ).astype(float)
    df["is_elderly"] = (df["age"] >= 65).astype(int)
    df["is_pediatric"] = (df["age"] <= 12).astype(int)

    return df


def one_hot_frame(df: pd.DataFrame, columns: Iterable[str]) -> tuple[pd.DataFrame, dict]:
    columns = [col for col in columns if col in df.columns]
    if not columns:
        return pd.DataFrame(index=df.index), {"columns": [], "categories": {}}

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded = encoder.fit_transform(df[columns].fillna("missing").astype(str))
    names = encoder.get_feature_names_out(columns)
    meta = {
        "columns": columns,
        "categories": {
            col: [str(item) for item in cats] for col, cats in zip(columns, encoder.categories_)
        },
    }
    return pd.DataFrame(encoded, columns=names, index=df.index), meta


def build_feature_matrix(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = add_clinical_features(df)

    clinical_features = [
        "age",
        "age_group",
        "is_elderly",
        "is_pediatric",
        "triage_vital_hr",
        "triage_vital_sbp",
        "triage_vital_dbp",
        "triage_vital_rr",
        "triage_vital_o2sat",
        "triage_vital_temp",
        "shock_index",
        "map",
        "pulse_pressure",
        "hr_rr_ratio",
        "hr_abnormal",
        "sbp_abnormal",
        "rr_abnormal",
        "o2_abnormal",
        "temp_abnormal",
        "map_abnormal",
        "shock_index_abnormal",
        "vital_severity_score",
    ]
    clinical_features = [feature for feature in clinical_features if feature in df.columns]

    numeric_context_features = []
    for col in ["n_edvisits", "n_admissions"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            numeric_context_features.append(col)

    categorical_frame, categorical_meta = one_hot_frame(
        df,
        [
            "dep_name",
            "gender",
            "arrivalmode",
            "arrivalmonth",
            "arrivalday",
            "arrivalhour_bin",
            "previousdispo",
            "triage_vital_o2_device",
        ],
    )

    cc_cols = []
    for col in df.columns:
        if col.startswith("cc_"):
            values = pd.to_numeric(df[col], errors="coerce").fillna(0)
            if values.mean() >= MIN_CC_PREVALENCE:
                df[col] = values.clip(0, 1)
                cc_cols.append(col)

    X = pd.concat(
        [df[clinical_features + numeric_context_features], categorical_frame, df[cc_cols]],
        axis=1,
    )
    X = X.replace([np.inf, -np.inf], np.nan)

    metadata = {
        "clinical_features": clinical_features,
        "numeric_context_features": numeric_context_features,
        "categorical": categorical_meta,
        "chief_complaint_features": cc_cols,
        "feature_count": X.shape[1],
        "target": "esi <= 2",
        "excluded_for_leakage_control": [
            "labs after triage",
            "medications",
            "imaging counts",
            "disposition",
            "diagnosis groups not available at first triage",
            "race and ethnicity until subgroup fairness is reviewed",
        ],
    }
    return X, metadata


def choose_threshold(
    y_true: np.ndarray, proba: np.ndarray, target_recall: float
) -> tuple[float, dict]:
    precision, recall, thresholds = precision_recall_curve(y_true, proba)
    candidates = []
    for p, r, t in zip(precision[:-1], recall[:-1], thresholds):
        if r >= target_recall:
            candidates.append((p, r, t))

    if candidates:
        best_precision, best_recall, best_threshold = max(candidates, key=lambda item: item[0])
        strategy = "max_precision_at_target_recall"
    else:
        f1 = 2 * precision[:-1] * recall[:-1] / (precision[:-1] + recall[:-1] + 1e-9)
        idx = int(np.argmax(f1))
        best_precision = float(precision[idx])
        best_recall = float(recall[idx])
        best_threshold = float(thresholds[idx])
        strategy = "fallback_best_f1"

    return float(best_threshold), {
        "strategy": strategy,
        "validation_precision": float(best_precision),
        "validation_recall": float(best_recall),
        "target_recall": target_recall,
    }


def evaluate_split(y_true: np.ndarray, proba: np.ndarray, threshold: float) -> SplitMetrics:
    y_pred = (proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    fpr = fp / (fp + tn) if (fp + tn) else 0.0
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    return SplitMetrics(
        auc=float(roc_auc_score(y_true, proba)),
        average_precision=float(average_precision_score(y_true, proba)),
        threshold=float(threshold),
        precision=float(precision),
        recall=float(recall),
        f1=float(f1),
        fpr=float(fpr),
        specificity=float(specificity),
        tp=int(tp),
        fp=int(fp),
        tn=int(tn),
        fn=int(fn),
    )


def train_models(X_train: np.ndarray, y_train: pd.Series) -> dict:
    neg = int((y_train == 0).sum())
    pos = int((y_train == 1).sum())
    scale_pos_weight = neg / max(pos, 1)

    models = {
        "random_forest": RandomForestClassifier(
            n_estimators=350,
            max_depth=18,
            min_samples_leaf=8,
            max_features="sqrt",
            class_weight="balanced_subsample",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "extra_trees": ExtraTreesClassifier(
            n_estimators=450,
            max_depth=20,
            min_samples_leaf=6,
            max_features="sqrt",
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }

    if xgb is not None:
        models["xgboost"] = xgb.XGBClassifier(
            n_estimators=650,
            max_depth=5,
            learning_rate=0.03,
            subsample=0.85,
            colsample_bytree=0.85,
            min_child_weight=8,
            reg_lambda=2.0,
            reg_alpha=0.1,
            scale_pos_weight=scale_pos_weight,
            objective="binary:logistic",
            eval_metric="aucpr",
            random_state=RANDOM_STATE,
            n_jobs=-1,
            tree_method="hist",
            verbosity=0,
        )

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)

    return models


def weighted_ensemble(models: dict, X: np.ndarray, weights: dict) -> np.ndarray:
    proba = np.zeros(X.shape[0])
    for name, model in models.items():
        proba += weights[name] * model.predict_proba(X)[:, 1]
    return proba


def make_weights(models: dict, X_val: np.ndarray, y_val: pd.Series) -> tuple[dict, dict]:
    aucs = {
        name: float(roc_auc_score(y_val, model.predict_proba(X_val)[:, 1]))
        for name, model in models.items()
    }
    raw_weights = {name: max(auc, 0.5) ** 4 for name, auc in aucs.items()}
    total = sum(raw_weights.values())
    weights = {name: weight / total for name, weight in raw_weights.items()}
    return weights, aucs


def select_predictor(
    models: dict, weights: dict, X_val: np.ndarray, y_val: pd.Series
) -> tuple[str, dict, dict]:
    candidates = {
        "weighted_ensemble": {
            "weights": weights,
            "proba": weighted_ensemble(models, X_val, weights),
        }
    }
    for name, model in models.items():
        single_weights = {model_name: 0.0 for model_name in models}
        single_weights[name] = 1.0
        candidates[name] = {
            "weights": single_weights,
            "proba": model.predict_proba(X_val)[:, 1],
        }

    candidate_auc = {
        name: float(roc_auc_score(y_val, info["proba"]))
        for name, info in candidates.items()
    }
    selected_name = max(candidate_auc, key=candidate_auc.get)
    return selected_name, candidates[selected_name]["weights"], candidate_auc


def save_confusion_matrix(cm: np.ndarray, metrics: SplitMetrics) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap=plt.cm.Blues)
    plt.colorbar(im, ax=ax)
    ax.set(
        xticks=[0, 1],
        yticks=[0, 1],
        xticklabels=["Non-critical", "Critical"],
        yticklabels=["Non-critical", "Critical"],
        ylabel="True label",
        xlabel="Predicted label",
        title=f"Confusion Matrix - v5 (AUC={metrics.auc:.3f})",
    )
    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black",
                fontsize=14,
            )
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "confusion_matrix_v5.png", dpi=160)
    plt.close(fig)


def save_confidence_plot(y_true: np.ndarray, proba: np.ndarray, threshold: float) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(proba[y_true == 0], bins=50, alpha=0.65, label="Non-critical", color="#2f6f9f")
    ax.hist(proba[y_true == 1], bins=50, alpha=0.65, label="Critical", color="#c84b31")
    ax.axvline(threshold, color="black", linestyle="--", label=f"Threshold={threshold:.3f}")
    ax.set(
        xlabel="Predicted probability",
        ylabel="Patient count",
        title="Confidence Distribution - Test Split",
    )
    ax.legend()
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "confidence_distribution_v5.png", dpi=160)
    plt.close(fig)


def save_shap_plot(models: dict, X_test: np.ndarray, feature_names: list[str]) -> None:
    if shap is None or "xgboost" not in models:
        print("Skipping SHAP plot; shap or xgboost is not installed.")
        return

    rng = np.random.default_rng(RANDOM_STATE)
    sample_idx = rng.choice(len(X_test), min(1000, len(X_test)), replace=False)
    explainer = shap.TreeExplainer(models["xgboost"])
    shap_values = explainer.shap_values(X_test[sample_idx])
    plt.figure(figsize=(10, 8))
    shap.summary_plot(
        shap_values,
        X_test[sample_idx],
        feature_names=feature_names,
        max_display=20,
        show=False,
    )
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "shap_summary_v5.png", dpi=160, bbox_inches="tight")
    plt.close()


def main(sample_rows: int | None = None) -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    usecols = training_usecols(DATA_PATH)
    df = pd.read_csv(DATA_PATH, usecols=usecols, low_memory=False)
    if sample_rows:
        df = df.sample(n=min(sample_rows, len(df)), random_state=RANDOM_STATE)
    print(f"Raw data: {df.shape}")

    df = df.dropna(subset=["esi"])
    df["esi"] = pd.to_numeric(df["esi"], errors="coerce")
    df = df[df["esi"].between(1, 5)]
    df["target"] = (df["esi"] <= 2).astype(int)
    print(f"Filtered data: {df.shape}; critical rate: {df['target'].mean():.2%}")

    X, feature_metadata = build_feature_matrix(df)
    y = df["target"]
    print(f"Feature matrix: {X.shape}")

    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval,
        y_trainval,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y_trainval,
    )

    imputer = SimpleImputer(strategy="median")
    scaler = RobustScaler(with_centering=False)
    X_train_np = scaler.fit_transform(imputer.fit_transform(X_train))
    X_val_np = scaler.transform(imputer.transform(X_val))
    X_test_np = scaler.transform(imputer.transform(X_test))

    models = train_models(X_train_np, y_train)
    weights, validation_model_auc = make_weights(models, X_val_np, y_val)
    selected_predictor, selected_weights, validation_candidate_auc = select_predictor(
        models, weights, X_val_np, y_val
    )
    print(f"Validation model AUCs: {validation_model_auc}")
    print(f"Default ensemble weights: {weights}")
    print(f"Validation candidate AUCs: {validation_candidate_auc}")
    print(f"Selected predictor: {selected_predictor}; weights: {selected_weights}")

    val_proba = weighted_ensemble(models, X_val_np, selected_weights)
    threshold, threshold_info = choose_threshold(y_val.to_numpy(), val_proba, TARGET_RECALL)
    test_proba = weighted_ensemble(models, X_test_np, selected_weights)
    test_metrics = evaluate_split(y_test.to_numpy(), test_proba, threshold)
    val_metrics = evaluate_split(y_val.to_numpy(), val_proba, threshold)

    y_test_pred = (test_proba >= threshold).astype(int)
    print("\nValidation metrics")
    print(json.dumps(asdict(val_metrics), indent=2))
    print("\nTest classification report")
    print(classification_report(y_test, y_test_pred, target_names=["Non-critical", "Critical"]))
    print("\nTest metrics")
    print(json.dumps(asdict(test_metrics), indent=2))

    cm = confusion_matrix(y_test, y_test_pred)
    save_confusion_matrix(cm, test_metrics)
    save_confidence_plot(y_test.to_numpy(), test_proba, threshold)
    save_shap_plot(models, X_test_np, list(X.columns))

    metrics_report = {
        "version": "v5",
        "created_by": "ml/train.py",
        "target_definition": "critical = ESI 1 or ESI 2",
        "target_recall": TARGET_RECALL,
        "dataset": {
            "path": str(DATA_PATH.relative_to(ROOT)),
            "rows_after_filter": int(len(df)),
            "critical_rate": float(y.mean()),
            "train_rows": int(len(y_train)),
            "validation_rows": int(len(y_val)),
            "test_rows": int(len(y_test)),
        },
        "feature_metadata": feature_metadata,
        "validation_model_auc": validation_model_auc,
        "validation_candidate_auc": validation_candidate_auc,
        "default_ensemble_weights": weights,
        "selected_predictor": selected_predictor,
        "selected_weights": selected_weights,
        "threshold_selection": threshold_info,
        "validation_metrics": asdict(val_metrics),
        "test_metrics": asdict(test_metrics),
    }

    METRICS_PATH.write_text(json.dumps(metrics_report, indent=2), encoding="utf-8")

    artifact = {
        "version": "v5",
        "models": models,
        "weights": selected_weights,
        "default_ensemble_weights": weights,
        "selected_predictor": selected_predictor,
        "threshold": threshold,
        "feature_names": list(X.columns),
        "feature_metadata": feature_metadata,
        "imputer": imputer,
        "scaler": scaler,
        "metrics": metrics_report,
    }
    with MODEL_PATH.open("wb") as f:
        pickle.dump(artifact, f)

    print(f"\nSaved model: {MODEL_PATH.relative_to(ROOT)}")
    print(f"Saved metrics: {METRICS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sample-rows",
        type=int,
        default=None,
        help="Optional fast smoke-test sample size. Omit for final training.",
    )
    args = parser.parse_args()
    main(sample_rows=args.sample_rows)
