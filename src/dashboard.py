"""Customer analytics dashboard using Streamlit."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import joblib
import sys

sys.path.insert(0, str(Path(__file__).parent))
from processing import load_data, build_features, FEATURE_COLS

DATA_DIR = Path(__file__).parent.parent / "data"
MODEL_DIR = Path(__file__).parent.parent / "models"

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide", page_icon="📊")


@st.cache_data
def load_scored_data():
    path = DATA_DIR / "customer_scores.csv"
    if path.exists():
        return pd.read_csv(path)
    return None


@st.cache_data
def load_full_data():
    riders, trips, sessions, drivers, _ = load_data()
    df = build_features(riders, trips, sessions)
    return df


def kpi_cards(df):
    total = len(df)
    high_risk = (df["risk_tier"] == "High Risk").sum() if "risk_tier" in df else 0
    med_risk = (df["risk_tier"] == "Medium Risk").sum() if "risk_tier" in df else 0
    avg_score = df["churn_score"].mean() if "churn_score" in df else 0
    total_spend = df["total_spend"].sum() if "total_spend" in df else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Customers", f"{total:,}")
    c2.metric("High Risk", f"{high_risk:,}", f"{high_risk/total:.1%}")
    c3.metric("Medium Risk", f"{med_risk:,}", f"{med_risk/total:.1%}")
    c4.metric("Avg Churn Score", f"{avg_score:.2f}")
    c5.metric("Total Revenue at Risk", f"${total_spend * avg_score:,.0f}")


def churn_distribution(df):
    fig = px.histogram(
        df, x="churn_score", nbins=50, color_discrete_sequence=["#636EFA"],
        title="Churn Score Distribution",
        labels={"churn_score": "Churn Probability Score"},
    )
    fig.add_vline(x=0.3, line_dash="dash", line_color="orange", annotation_text="Medium Risk")
    fig.add_vline(x=0.6, line_dash="dash", line_color="red", annotation_text="High Risk")
    return fig


def segment_breakdown(df):
    if "segment_label" not in df.columns:
        return None
    seg = df.groupby("segment_label").agg(
        customers=("user_id", "count"),
        avg_churn=("churn_score", "mean"),
        avg_spend=("total_spend", "mean"),
    ).reset_index()
    fig = px.bar(
        seg, x="segment_label", y="customers", color="avg_churn",
        color_continuous_scale="RdYlGn_r",
        title="Customers by Segment",
        labels={"customers": "# Customers", "segment_label": "Segment", "avg_churn": "Avg Churn Score"},
    )
    return fig


def spend_vs_churn(df):
    sample = df.sample(min(2000, len(df)), random_state=42)
    fig = px.scatter(
        sample, x="total_spend", y="churn_score",
        color="risk_tier" if "risk_tier" in df else None,
        color_discrete_map={"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"},
        title="Spend vs Churn Risk",
        labels={"total_spend": "Total Spend ($)", "churn_score": "Churn Score"},
        opacity=0.6,
    )
    return fig


def top_at_risk(df):
    cols = ["user_id", "churn_score", "risk_tier", "segment_label", "total_spend", "trip_count"]
    available = [c for c in cols if c in df.columns]
    return df[available].sort_values("churn_score", ascending=False).head(20)


def main():
    st.title("📊 Customer Churn & Analytics Dashboard")
    st.markdown("Real-time risk assessment and customer segmentation insights")

    df = load_scored_data()
    if df is None:
        st.warning("No scored data found. Please run `python src/model.py` first.")
        st.stop()

    st.subheader("Key Metrics")
    kpi_cards(df)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(churn_distribution(df), use_container_width=True)
    with col2:
        fig = segment_breakdown(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(spend_vs_churn(df), use_container_width=True)
    with col4:
        if "risk_tier" in df.columns:
            risk_counts = df["risk_tier"].value_counts().reset_index()
            risk_counts.columns = ["Risk Tier", "Count"]
            fig = px.pie(risk_counts, names="Risk Tier", values="Count",
                         color="Risk Tier",
                         color_discrete_map={"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"},
                         title="Risk Tier Distribution")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 20 Customers At Risk")
    st.dataframe(top_at_risk(df), use_container_width=True)

    st.subheader("Filter & Explore")
    if "risk_tier" in df.columns:
        tier_filter = st.multiselect("Risk Tier", df["risk_tier"].unique(), default=list(df["risk_tier"].unique()))
        filtered = df[df["risk_tier"].isin(tier_filter)]
        st.dataframe(filtered.sort_values("churn_score", ascending=False).head(100), use_container_width=True)


if __name__ == "__main__":
    main()
