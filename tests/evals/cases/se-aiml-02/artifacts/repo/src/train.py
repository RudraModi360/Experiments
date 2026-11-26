import csv
import json
import math
import random
from pathlib import Path
from src.features import FEATURE_NAMES, extract_features
from src.metrics import roc_auc

ROOT = Path(__file__).resolve().parents[1]


def sigmoid(z: float) -> float:
    z = max(-30.0, min(30.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def fit_logreg(X: list[list[float]], y: list[int], lr: float = 0.4, epochs: int = 350) -> tuple[list[float], float]:
    n_feat = len(X[0])
    w = [0.0] * n_feat
    b = 0.0
    n = len(X)
    for _ in range(epochs):
        gw = [0.0] * n_feat
        gb = 0.0
        for xi, yi in zip(X, y):
            p = sigmoid(sum(wj * xj for wj, xj in zip(w, xi)) + b)
            err = p - yi
            gb += err
            for j in range(n_feat):
                gw[j] += err * xi[j]
        b -= lr * gb / n
        for j in range(n_feat):
            w[j] -= lr * (gw[j] / n + 0.001 * w[j])
    return w, b


def train_model(train_csv: Path | None = None, out_path: Path | None = None) -> dict:
    train_csv = train_csv or (ROOT / "data" / "train.csv")
    out_path = out_path or (ROOT / "model.json")
    with train_csv.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    # BUG: random split instead of chronological split
    rng = random.Random(7)
    rng.shuffle(rows)
    cut = int(len(rows) * 0.8)
    tr_rows, va_rows = rows[:cut], rows[cut:]
    X_tr = [extract_features(r) for r in tr_rows]
    y_tr = [int(r["churned"]) for r in tr_rows]
    X_va = [extract_features(r) for r in va_rows]
    y_va = [int(r["churned"]) for r in va_rows]
    w, b = fit_logreg(X_tr, y_tr)
    val_scores = [sigmoid(sum(wj * xj for wj, xj in zip(w, xi)) + b) for xi in X_va]
    artifact = {
        "features": FEATURE_NAMES,
        "weights": w,
        "bias": b,
        "spend_median": 150.0,
        "val_auc": round(roc_auc(y_va, val_scores), 4),
        "split_strategy": "random",
    }
    out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    return artifact


if __name__ == "__main__":
    res = train_model()
    print(json.dumps(res, indent=2))
