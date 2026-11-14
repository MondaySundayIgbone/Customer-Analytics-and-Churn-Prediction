"""Churn prediction models, segmentation, interpretability, and scoring."""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report, roc_auc_score, confusion_matrix,
    precision_recall_curve, average_precision_score,
)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import joblib
from pathlib import Path

from processing import build_features, load_data, FEATURE_COLS, TARGET_COL

MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)


# ── 1. Train churn models ────────────────────────────────────────────────────

def train_models(df: pd.DataFrame):
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "logistic_regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]),
        "random_forest": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                           random_state=42, n_jobs=-1)),
        ]),
        "gradient_boosting": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", GradientBoostingClassifier(n_estimators=200, learning_rate=0.05,
                                               max_depth=4, random_state=42)),
        ]),
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, pipe in models.items():
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]

        cv_auc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc").mean()
        test_auc = roc_auc_score(y_test, y_prob)
        ap = average_precision_score(y_test, y_prob)

        results[name] = {
            "pipeline": pipe,
            "cv_auc": cv_auc,
            "test_auc": test_auc,
            "avg_precision": ap,
            "report": classification_report(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
        }

        joblib.dump(pipe, MODEL_DIR / f"{name}.pkl")
        print(f"{name:25s} | CV AUC: {cv_auc:.4f} | Test AUC: {test_auc:.4f} | AP: {ap:.4f}")

    # Best model
    best_name = max(results, key=lambda k: results[k]["test_auc"])
    print(f"\nBest model: {best_name} (AUC={results[best_name]['test_auc']:.4f})")
    return results, best_name, X_test, y_test


# ── 2. Customer segmentation ─────────────────────────────────────────────────

SEGMENT_FEATURES = [
    "trip_count", "total_spend", "avg_spend_per_trip",
    "days_since_last_trip", "conversion_rate", "churn_prob",
]


def build_segments(df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    seg_df = df[["user_id"] + SEGMENT_FEATURES].copy().fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(seg_df[SEGMENT_FEATURES])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    seg_df["segment"] = kmeans.fit_predict(X_scaled)

    joblib.dump({"kmeans": kmeans, "scaler": scaler}, MODEL_DIR / "segmentation.pkl")

    # Label segments by churn risk + value
    seg_summary = seg_df.groupby("segment")[SEGMENT_FEATURES].mean()
    print("\nSegment Profiles:")
    print(seg_summary.round(2))

    segment_labels = _label_segments(seg_summary)
    seg_df["segment_label"] = seg_df["segment"].map(segment_labels)
    return seg_df[["user_id", "segment", "segment_label"]]


def _label_segments(summary: pd.DataFrame) -> dict:
    labels = {}
    for idx, row in summary.iterrows():
        if row["churn_prob"] > 0.6 and row["total_spend"] < summary["total_spend"].median():
            labels[idx] = "High Risk - Low Value"
        elif row["churn_prob"] > 0.6 and row["total_spend"] >= summary["total_spend"].median():
            labels[idx] = "High Risk - High Value"
        elif row["churn_prob"] <= 0.6 and row["total_spend"] >= summary["total_spend"].median():
            labels[idx] = "Low Risk - High Value"
        else:
            labels[idx] = "Low Risk - Low Value"
    return labels


# ── 3. Model interpretability ────────────────────────────────────────────────

def explain_model(results: dict, best_name: str, df: pd.DataFrame):
    pipe = results[best_name]["pipeline"]
    clf = pipe.named_steps["clf"]

    if hasattr(clf, "feature_importances_"):
        importances = clf.feature_importances_
    elif hasattr(clf, "coef_"):
        importances = np.abs(clf.coef_[0])
    else:
        return pd.DataFrame()

    feat_imp = pd.DataFrame({
        "feature": FEATURE_COLS,
        "importance": importances,
    }).sort_values("importance", ascending=False)

    # Business-friendly descriptions
    business_names = {
        "days_since_last_trip": "Days inactive (no trips)",
        "churn_prob": "Model churn probability",
        "trip_count": "Total trips taken",
        "total_spend": "Lifetime spend ($)",
        "loyalty_rank": "Loyalty tier (Bronze→Platinum)",
        "conversion_rate": "App session conversion rate",
        "avg_spend_per_trip": "Average spend per trip ($)",
        "avg_time_on_app": "Avg time spent in app (min)",
        "trips_per_week": "Trip frequency (per week)",
        "surge_trip_rate": "% trips during surge pricing",
    }
    feat_imp["business_label"] = feat_imp["feature"].map(business_names).fillna(feat_imp["feature"])

    print("\nTop 10 Churn Drivers:")
    print(feat_imp.head(10)[["business_label", "importance"]].to_string(index=False))
    return feat_imp


# ── 4. Real-time scoring ─────────────────────────────────────────────────────

def score_customers(df: pd.DataFrame, model_name: str = None) -> pd.DataFrame:
    if model_name is None:
        # pick best available
        candidates = list(MODEL_DIR.glob("*.pkl"))
        model_files = [f for f in candidates if "segmentation" not in f.name]
        if not model_files:
            raise FileNotFoundError("No trained models found. Run train_models() first.")
        model_name = model_files[0].stem

    pipe = joblib.load(MODEL_DIR / f"{model_name}.pkl")
    X = df[FEATURE_COLS].fillna(0)

    scores = pipe.predict_proba(X)[:, 1]
    risk_labels = pd.cut(scores, bins=[0, 0.3, 0.6, 1.0],
                         labels=["Low Risk", "Medium Risk", "High Risk"])

    result = df[["user_id"]].copy()
    result["churn_score"] = scores.round(4)
    result["risk_tier"] = risk_labels
    result["intervention_priority"] = (scores * 100).round(0).astype(int)
    return result.sort_values("churn_score", ascending=False)


# ── 5. Entrypoint ────────────────────────────────────────────────────────────

def run_pipeline():
    print("=" * 60)
    print("CUSTOMER CHURN PREDICTION PIPELINE")
    print("=" * 60)

    print("\n[1] Loading & engineering features...")
    riders, trips, sessions, drivers, promotions = load_data()
    df = build_features(riders, trips, sessions)
    print(f"    Dataset: {df.shape[0]} customers, {len(FEATURE_COLS)} features")
    print(f"    Churn rate: {df[TARGET_COL].mean():.1%}")

    print("\n[2] Training churn models...")
    results, best_name, X_test, y_test = train_models(df)

    print("\n[3] Classification report (best model):")
    print(results[best_name]["report"])

    print("\n[4] Building customer segments...")
    seg_df = build_segments(df)
    print(seg_df["segment_label"].value_counts().to_string())

    print("\n[5] Feature importance (interpretability)...")
    feat_imp = explain_model(results, best_name, df)

    print("\n[6] Scoring all customers...")
    scores_df = score_customers(df, best_name)
    df = df.merge(seg_df[["user_id", "segment_label"]], on="user_id", how="left")
    df = df.merge(scores_df[["user_id", "churn_score", "risk_tier"]], on="user_id", how="left")

    output_path = Path(__file__).parent.parent / "data" / "customer_scores.csv"
    df[["user_id", "churn_score", "risk_tier", "segment_label", "total_spend",
        "trip_count", "days_since_last_trip"]].to_csv(output_path, index=False)
    print(f"\n    Scores saved to: {output_path}")

    print("\n[7] Risk tier distribution:")
    print(scores_df["risk_tier"].value_counts().to_string())

    return df, results, best_name, feat_imp


if __name__ == "__main__":
    run_pipeline()
