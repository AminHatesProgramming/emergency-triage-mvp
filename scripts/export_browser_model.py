from __future__ import annotations

import json
import pickle
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "triage_model_v7.pkl"
OUT_PATH = ROOT / "frontend" / "model-v7.json"


def floats(values) -> list[float]:
    return [float(value) for value in values]


def main() -> None:
    with MODEL_PATH.open("rb") as f:
        artifact = pickle.load(f)

    selected = artifact["selected_predictor"]
    model = artifact["models"][selected]
    booster = model.get_booster()

    payload = {
        "version": artifact["version"],
        "selected_predictor": selected,
        "threshold": float(artifact["threshold"]),
        "feature_names": artifact["feature_names"],
        "feature_metadata": artifact["feature_metadata"],
        "imputer_statistics": floats(artifact["imputer"].statistics_),
        "scaler_scale": floats(artifact["scaler"].scale_),
        "trees": [json.loads(tree) for tree in booster.get_dump(dump_format="json")],
        "metrics": artifact["metrics"].get("test_metrics", {}),
        "operating_points": artifact["metrics"].get("operating_points", {}),
        "decision_support_only": True,
    }

    OUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Exported browser model: {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
