"""REST API for real-time churn scoring (FastAPI)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import uvicorn

from processing import FEATURE_COLS

MODEL_DIR = Path(__file__).parent.parent / "models"

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Real-time churn risk scoring for ride-hailing customers",
    version="1.0.0",
)

# Load best model at startup
_model = None


def get_model():
    global _model
    if _model is None:
        candidates = [f for f in MODEL_DIR.glob("*.pkl") if "segmentation" not in f.name]
        if not candidates:
            raise FileNotFoundError("No trained models. Run model.py first.")
        # prefer gradient_boosting > random_forest > logistic_regression
        priority = ["gradient_boosting", "random_forest", "logistic_regression"]
        for name in priority:
            path = MODEL_DIR / f"{name}.pkl"
            if path.exists():
                _model = joblib.load(path)
                break
        if _model is None:
            _model = joblib.load(candidates[0])
    return _model


class CustomerFeatures(BaseModel):
    user_id: str
    age: float = 30
    loyalty_rank: float = 0
    has_referral: float = 0
    age_group: float = 1
    avg_rating_given: float = 4.5
    trip_count: float = 0
    total_spend: float = 0
    avg_spend_per_trip: float = 0
    avg_trip_duration: float = 0
    avg_fare: float = 0
    avg_tip: float = 0
    surge_trip_rate: float = 0
    weekend_trip_rate: float = 0
    days_since_last_trip: float = 0
    customer_tenure_days: float = 0
    trips_per_week: float = 0
    unique_cities: float = 1
    cash_payment_rate: float = 0
    session_count: float = 0
    avg_time_on_app: float = 0
    avg_pages_visited: float = 0
    conversion_rate: float = 0


class ScoreResponse(BaseModel):
    user_id: str
    churn_score: float
    risk_tier: str
    intervention_priority: int
    recommendation: str


def _risk_tier(score: float) -> str:
    if score < 0.3:
        return "Low Risk"
    elif score < 0.6:
        return "Medium Risk"
    return "High Risk"


def _recommendation(score: float, features: dict) -> str:
    if score >= 0.6:
        if features.get("days_since_last_trip", 0) > 30:
            return "Send win-back promo — customer inactive for 30+ days"
        return "Immediate outreach: offer loyalty upgrade or discount"
    elif score >= 0.3:
        return "Enroll in loyalty program or send engagement notification"
    return "No action needed — low churn risk"


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _model is not None}


@app.post("/score", response_model=ScoreResponse)
def score_customer(customer: CustomerFeatures):
    try:
        model = get_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    features = customer.dict()
    user_id = features.pop("user_id")
    X = pd.DataFrame([features])[FEATURE_COLS]

    prob = float(model.predict_proba(X)[0, 1])
    tier = _risk_tier(prob)
    rec = _recommendation(prob, features)

    return ScoreResponse(
        user_id=user_id,
        churn_score=round(prob, 4),
        risk_tier=tier,
        intervention_priority=int(prob * 100),
        recommendation=rec,
    )


@app.post("/score/batch")
def score_batch(customers: list[CustomerFeatures]):
    if len(customers) > 1000:
        raise HTTPException(status_code=400, detail="Batch size limit is 1000")
    return [score_customer(c) for c in customers]


@app.get("/segments/summary")
def segments_summary():
    seg_path = Path(__file__).parent.parent / "data" / "customer_scores.csv"
    if not seg_path.exists():
        raise HTTPException(status_code=404, detail="Run the pipeline first to generate scores")
    df = pd.read_csv(seg_path)
    summary = df.groupby("segment_label").agg(
        customer_count=("user_id", "count"),
        avg_churn_score=("churn_score", "mean"),
        avg_spend=("total_spend", "mean"),
        avg_trips=("trip_count", "mean"),
    ).round(2).reset_index()
    return summary.to_dict(orient="records")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
