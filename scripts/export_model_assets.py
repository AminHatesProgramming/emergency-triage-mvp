from __future__ import annotations

import json
import pickle
import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import auc, precision_recall_curve, roc_curve
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ml.train import DATA_PATH, RANDOM_STATE, build_feature_matrix, training_usecols

REPORT_DIR = ROOT / "reports" / "model"
POSTER_DIR = ROOT / "poster-assets"
MODEL_PATH = ROOT / "models" / "triage_model_v7.pkl"
METRICS_PATH = REPORT_DIR / "metrics_v7.json"


def load_test_split() -> tuple[pd.DataFrame, pd.Series]:
    usecols = training_usecols(DATA_PATH)
    df = pd.read_csv(DATA_PATH, usecols=usecols)
    df = df.dropna(subset=["esi"])
    df["esi"] = pd.to_numeric(df["esi"], errors="coerce")
    df = df[df["esi"].between(1, 5)]
    df["target"] = (df["esi"] <= 2).astype(int)
    X, _ = build_feature_matrix(df)
    y = df["target"]
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )
    return X_test, y_test


def predict_scores(X_test: pd.DataFrame) -> list[float]:
    with MODEL_PATH.open("rb") as f:
        artifact = pickle.load(f)

    X = X_test.reindex(columns=artifact["feature_names"], fill_value=0)
    X_np = artifact["scaler"].transform(artifact["imputer"].transform(X))
    proba = None
    for name, weight in artifact["weights"].items():
        if not weight or name not in artifact["models"]:
            continue
        scores = artifact["models"][name].predict_proba(X_np)[:, 1]
        proba = scores * weight if proba is None else proba + scores * weight
    if proba is None:
        raise RuntimeError("No weighted model was available in the artifact.")
    return proba


def save_roc(y_test: pd.Series, proba) -> None:
    fpr, tpr, _ = roc_curve(y_test, proba)
    roc_auc = auc(fpr, tpr)
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.plot(fpr, tpr, color="#087f8c", linewidth=2.5, label=f"AUC = {roc_auc:.4f}")
    ax.plot([0, 1], [0, 1], color="#7a8790", linestyle="--", linewidth=1.2)
    ax.set(
        title="ROC Curve - v7 Test Split",
        xlabel="False Positive Rate",
        ylabel="True Positive Rate",
        xlim=(0, 1),
        ylim=(0, 1),
    )
    ax.grid(alpha=0.22)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "roc_curve_v7.png", dpi=180)
    fig.savefig(POSTER_DIR / "roc-curve.png", dpi=180)
    plt.close(fig)


def save_pr(y_test: pd.Series, proba) -> None:
    precision, recall, _ = precision_recall_curve(y_test, proba)
    pr_auc = auc(recall, precision)
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.plot(recall, precision, color="#575bc3", linewidth=2.5, label=f"AP/AUC = {pr_auc:.4f}")
    ax.set(
        title="Precision-Recall Curve - v7 Test Split",
        xlabel="Recall",
        ylabel="Precision",
        xlim=(0, 1),
        ylim=(0, 1),
    )
    ax.grid(alpha=0.22)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "precision_recall_curve_v7.png", dpi=180)
    fig.savefig(POSTER_DIR / "precision-recall-curve.png", dpi=180)
    plt.close(fig)


def save_version_comparison() -> None:
    versions = [
        ("v2", 0.8467, None, None, 0.4870),
        ("v3", 0.8467, None, None, None),
        ("v5", 0.8917, 0.9194, 0.5275, 0.3572),
    ]
    with METRICS_PATH.open(encoding="utf-8") as f:
        metrics = json.load(f)["test_metrics"]
    versions.append(
        (
            "v7",
            metrics["auc"],
            metrics["recall"],
            metrics["precision"],
            metrics["fpr"],
        )
    )

    labels = [item[0] for item in versions]
    auc_values = [item[1] for item in versions]
    recall_values = [item[2] for item in versions]
    fpr_values = [item[4] for item in versions]

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.plot(labels, auc_values, marker="o", linewidth=2.4, label="AUC", color="#087f8c")
    ax.plot(labels, recall_values, marker="o", linewidth=2.4, label="Recall", color="#157a55")
    ax.plot(labels, fpr_values, marker="o", linewidth=2.4, label="FPR", color="#c43b3b")
    ax.set_ylim(0.3, 1.0)
    ax.set_title("Model Version Comparison")
    ax.set_ylabel("Metric value")
    ax.grid(alpha=0.22)
    ax.legend()
    fig.tight_layout()
    fig.savefig(POSTER_DIR / "model-version-comparison.png", dpi=180)
    plt.close(fig)


def copy_static_assets() -> None:
    pairs = {
        REPORT_DIR / "confusion_matrix_v7.png": POSTER_DIR / "confusion-matrix.png",
        REPORT_DIR / "shap_summary_v7.png": POSTER_DIR / "feature-importance.png",
        REPORT_DIR / "confidence_distribution_v7.png": POSTER_DIR / "confidence-distribution.png",
    }
    for source, target in pairs.items():
        if source.exists():
            shutil.copyfile(source, target)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    POSTER_DIR.mkdir(parents=True, exist_ok=True)
    X_test, y_test = load_test_split()
    proba = predict_scores(X_test)
    save_roc(y_test, proba)
    save_pr(y_test, proba)
    save_version_comparison()
    copy_static_assets()
    print("Exported v7 model charts and poster assets.")


if __name__ == "__main__":
    main()
