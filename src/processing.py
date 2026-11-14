"""Feature engineering pipeline for customer behavioral data."""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_data():
    riders = pd.read_csv(DATA_DIR / "riders.csv", parse_dates=["signup_date"])
    trips = pd.read_csv(DATA_DIR / "trips.csv")
    trips["pickup_time"] = pd.to_datetime(trips["pickup_time"], utc=True)
    trips["dropoff_time"] = pd.to_datetime(trips["dropoff_time"], utc=True)
    sessions = pd.read_csv(DATA_DIR / "sessions.csv")
    sessions["session_time"] = pd.to_datetime(sessions["session_time"], utc=True)
    drivers = pd.read_csv(DATA_DIR / "drivers.csv", parse_dates=["signup_date", "last_active"])
    promotions = pd.read_csv(DATA_DIR / "promotions.csv", parse_dates=["start_date", "end_date"])
    return riders, trips, sessions, drivers, promotions


def engineer_trip_features(trips: pd.DataFrame) -> pd.DataFrame:
    trips = trips.copy()
    trips["trip_duration_min"] = (
        (trips["dropoff_time"] - trips["pickup_time"]).dt.total_seconds() / 60
    )
    trips["total_paid"] = trips["fare"] + trips["tip"].fillna(0)
    trips["hour_of_day"] = trips["pickup_time"].dt.hour
    trips["day_of_week"] = trips["pickup_time"].dt.dayofweek
    trips["is_weekend"] = trips["day_of_week"].isin([5, 6]).astype(int)
    trips["is_surge"] = (trips["surge_multiplier"] > 1).astype(int)

    agg = trips.groupby("user_id").agg(
        trip_count=("trip_id", "count"),
        total_spend=("total_paid", "sum"),
        avg_spend_per_trip=("total_paid", "mean"),
        avg_trip_duration=("trip_duration_min", "mean"),
        avg_fare=("fare", "mean"),
        avg_tip=("tip", "mean"),
        surge_trip_rate=("is_surge", "mean"),
        weekend_trip_rate=("is_weekend", "mean"),
        peak_hour=(
            "hour_of_day",
            lambda x: x.value_counts().index[0] if len(x) > 0 else -1,
        ),
        unique_cities=("city", "nunique"),
        cash_payment_rate=(
            "payment_type",
            lambda x: (x == "cash").mean(),
        ),
        last_trip_date=("pickup_time", "max"),
        first_trip_date=("pickup_time", "min"),
    ).reset_index()

    reference_date = trips["pickup_time"].max()
    agg["days_since_last_trip"] = (reference_date - agg["last_trip_date"]).dt.days
    agg["customer_tenure_days"] = (agg["last_trip_date"] - agg["first_trip_date"]).dt.days
    agg["trips_per_week"] = agg["trip_count"] / ((agg["customer_tenure_days"] / 7).clip(lower=1))

    return agg.drop(columns=["last_trip_date", "first_trip_date"])


def engineer_session_features(sessions: pd.DataFrame) -> pd.DataFrame:
    agg = sessions.groupby("rider_id").agg(
        session_count=("session_id", "count"),
        avg_time_on_app=("time_on_app", "mean"),
        avg_pages_visited=("pages_visited", "mean"),
        conversion_rate=("converted", "mean"),
        total_sessions=("session_id", "count"),
    ).reset_index().rename(columns={"rider_id": "user_id"})
    return agg


def build_features(riders: pd.DataFrame, trips: pd.DataFrame, sessions: pd.DataFrame) -> pd.DataFrame:
    trip_feats = engineer_trip_features(trips)
    sess_feats = engineer_session_features(sessions)

    df = riders.merge(trip_feats, on="user_id", how="left")
    df = df.merge(sess_feats, on="user_id", how="left")

    # Encode categoricals
    df["loyalty_rank"] = df["loyalty_status"].map({"Bronze": 0, "Silver": 1, "Gold": 2, "Platinum": 3}).fillna(0)
    df["has_referral"] = df["referred_by"].notna().astype(int)
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 50, 100], labels=[0, 1, 2, 3]).astype(float)

    # Binary churn label (top 20% by churn_prob = churned)
    threshold = df["churn_prob"].quantile(0.80)
    df["churned"] = (df["churn_prob"] >= threshold).astype(int)

    # Fill missings for riders with no trips/sessions
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(0)

    return df


FEATURE_COLS = [
    "age", "loyalty_rank", "has_referral", "age_group", "avg_rating_given",
    "churn_prob",
    "trip_count", "total_spend", "avg_spend_per_trip", "avg_trip_duration",
    "avg_fare", "avg_tip", "surge_trip_rate", "weekend_trip_rate",
    "days_since_last_trip", "customer_tenure_days", "trips_per_week",
    "unique_cities", "cash_payment_rate",
    "session_count", "avg_time_on_app", "avg_pages_visited", "conversion_rate",
]

TARGET_COL = "churned"
