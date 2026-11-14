"""Basic model monitoring — data drift and performance tracking."""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

MONITOR_DIR = Path(__file__).parent.parent / "monitoring"
MONITOR_DIR.mkdir(exist_ok=True)

from processing import FEATURE_COLS


def compute_feature_stats(df: pd.DataFrame) -> dict:
    stats = {}
    for col in FEATURE_COLS:
        if col in df.columns:
            stats[col] = {
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "null_rate": float(df[col].isna().mean()),
            }
    return stats


def save_baseline(df: pd.DataFrame):
    stats = compute_feature_stats(df)
    path = MONITOR_DIR / "baseline_stats.json"
    with open(path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Baseline stats saved to {path}")


def detect_drift(current_df: pd.DataFrame, threshold: float = 0.2) -> pd.DataFrame:
    baseline_path = MONITOR_DIR / "baseline_stats.json"
    if not baseline_path.exists():
        print("No baseline found. Run save_baseline() first.")
        return pd.DataFrame()

    with open(baseline_path) as f:
        baseline = json.load(f)

    current_stats = compute_feature_stats(current_df)
    drift_report = []

    for col in FEATURE_COLS:
        if col not in baseline or col not in current_stats:
            continue
        b_mean = baseline[col]["mean"]
        c_mean = current_stats[col]["mean"]
        b_std = baseline[col]["std"] if baseline[col]["std"] > 0 else 1e-9

        psi = abs(c_mean - b_mean) / b_std  # simplified drift score
        drift_report.append({
            "feature": col,
            "baseline_mean": round(b_mean, 4),
            "current_mean": round(c_mean, 4),
            "drift_score": round(psi, 4),
            "drift_detected": psi > threshold,
        })

    report_df = pd.DataFrame(drift_report).sort_values("drift_score", ascending=False)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_df.to_csv(MONITOR_DIR / f"drift_report_{timestamp}.csv", index=False)

    n_drifted = report_df["drift_detected"].sum()
    print(f"\nDrift Report: {n_drifted}/{len(FEATURE_COLS)} features drifted (threshold={threshold})")
    if n_drifted > 0:
        print(report_df[report_df["drift_detected"]][["feature", "drift_score"]].to_string(index=False))

    return report_df


def log_prediction_stats(scores_df: pd.DataFrame):
    stats = {
        "timestamp": datetime.now().isoformat(),
        "total_scored": len(scores_df),
        "avg_churn_score": float(scores_df["churn_score"].mean()),
        "high_risk_count": int((scores_df["risk_tier"] == "High Risk").sum()),
        "medium_risk_count": int((scores_df["risk_tier"] == "Medium Risk").sum()),
        "low_risk_count": int((scores_df["risk_tier"] == "Low Risk").sum()),
    }

    log_path = MONITOR_DIR / "prediction_log.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps(stats) + "\n")

    print(f"Logged prediction stats → {log_path}")
    print(f"  Avg score: {stats['avg_churn_score']:.3f} | High risk: {stats['high_risk_count']:,}")
    return stats


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from processing import load_data, build_features

    riders, trips, sessions, drivers, promotions = load_data()
    df = build_features(riders, trips, sessions)

    save_baseline(df)
    report = detect_drift(df)
    print("\nMonitoring baseline established.")
