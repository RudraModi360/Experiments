import csv
import json
import math
from pathlib import Path
from src.features import extract_features
from src.metrics import roc_auc

ROOT = Path(__file__).resolve().parents[1]


def sigmoid(z: float) -> float:
    z = max(-30.0, min(30.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def evaluate_holdout(holdout_csv: Path | None = None, model_path: Path | None = None) -> dict:
    holdout_csv = holdout_csv or (ROOT / "data" / "prod_holdout.csv")
    model_path = model_path or (ROOT / "model.json")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    w = model["weights"]
    b = model["bias"]
    spend_median = model.get("spend_median", 150.0)
    with holdout_csv.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    y_true, y_score = [], []
    for r in rows:
        x = extract_features(r, spend_median=spend_median)
        y_score.append(sigmoid(sum(wj * xj for wj, xj in zip(w, x)) + b))
        y_true.append(int(r["churned"]))
    return {"holdout_auc": round(roc_auc(y_true, y_score), 4), "n_rows": len(rows)}


if __name__ == "__main__":
    print(json.dumps(evaluate_holdout(), indent=2))
