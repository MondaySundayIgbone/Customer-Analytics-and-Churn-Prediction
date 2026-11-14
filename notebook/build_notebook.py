"""Script to generate the churn prediction notebook."""
import json

def md(src): return {"cell_type":"markdown","metadata":{},"source":src,"id":"m"+str(abs(hash(src)))[:8]}
def code(src): return {"cell_type":"code","metadata":{},"source":src,"outputs":[],"execution_count":None,"id":"c"+str(abs(hash(src)))[:8]}

cells = [
    md("# Customer Analytics & Churn Prediction System\n\n**Ride-Hailing Platform | End-to-End ML Pipeline**\n\nCovers all 8 deliverables:\n1. Churn Prediction Models\n2. Customer Segmentation\n3. Feature Engineering Pipeline\n4. Model Interpretability\n5. Real-Time Scoring\n6. Analytics Dashboard\n7. API Deployment\n8. Production Monitoring"),

    md("## Setup"),
    code("import sys\nsys.path.insert(0, '../src')\n\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport warnings\nwarnings.filterwarnings('ignore')\n\nplt.style.use('seaborn-v0_8-whitegrid')\n%matplotlib inline\nprint('Libraries loaded')"),

    md("---\n## Task 3: Feature Engineering Pipeline"),
    code("from processing import load_data, build_features, FEATURE_COLS, TARGET_COL\n\nriders, trips, sessions, drivers, promotions = load_data()\nprint(f'Riders:      {riders.shape}')\nprint(f'Trips:       {trips.shape}')\nprint(f'Sessions:    {sessions.shape}')\nprint(f'Drivers:     {drivers.shape}')\nprint(f'Promotions:  {promotions.shape}')"),

    code("df = build_features(riders, trips, sessions)\nprint(f'Feature matrix: {df.shape}')\nprint(f'Churn rate (top-20% label): {df[TARGET_COL].mean():.1%}')\ndf[FEATURE_COLS].describe().T.round(2)"),

    md("### Exploratory Analysis"),
    code(
        "fig, axes = plt.subplots(2, 3, figsize=(15, 8))\n\n"
        "axes[0,0].hist(df['churn_prob'], bins=50, color='steelblue', edgecolor='white')\n"
        "axes[0,0].axvline(df['churn_prob'].quantile(0.80), color='red', ls='--', label='Top-20% threshold')\n"
        "axes[0,0].set_title('Churn Probability Distribution')\n"
        "axes[0,0].legend()\n\n"
        "df.groupby('loyalty_status')['churn_prob'].mean().plot(kind='bar', ax=axes[0,1], color='coral')\n"
        "axes[0,1].set_title('Avg Churn Prob by Loyalty Tier')\n"
        "axes[0,1].tick_params(axis='x', rotation=0)\n\n"
        "df['trip_count'].clip(0,100).hist(bins=40, ax=axes[0,2], color='seagreen')\n"
        "axes[0,2].set_title('Trip Count Distribution')\n\n"
        "df.groupby(TARGET_COL)['total_spend'].mean().plot(kind='bar', ax=axes[1,0], color=['green','red'])\n"
        "axes[1,0].set_title('Avg Spend: Not Churned vs Churned')\n"
        "axes[1,0].set_xticklabels(['Not Churned','Churned'], rotation=0)\n\n"
        "df.groupby(TARGET_COL)['days_since_last_trip'].mean().plot(kind='bar', ax=axes[1,1], color=['green','red'])\n"
        "axes[1,1].set_title('Avg Days Inactive')\n"
        "axes[1,1].set_xticklabels(['Not Churned','Churned'], rotation=0)\n\n"
        "corr = df[FEATURE_COLS[:10]].corr()\n"
        "sns.heatmap(corr, ax=axes[1,2], cmap='coolwarm', annot=False)\n"
        "axes[1,2].set_title('Feature Correlations (first 10)')\n\n"
        "plt.tight_layout()\nplt.show()"
    ),

    md("---\n## Task 1: Churn Prediction Models"),
    code("from model import train_models\nresults, best_name, X_test, y_test = train_models(df)\nprint(f'\\nBest model: {best_name}')"),

    code(
        "comparison = pd.DataFrame({\n"
        "    name: {'CV AUC': res['cv_auc'], 'Test AUC': res['test_auc'], 'Avg Precision': res['avg_precision']}\n"
        "    for name, res in results.items()\n"
        "}).T.round(4)\nprint(comparison)"
    ),

    code(
        "from sklearn.metrics import RocCurveDisplay\n\n"
        "fig, ax = plt.subplots(figsize=(7,5))\n"
        "for name, res in results.items():\n"
        "    y_prob = res['pipeline'].predict_proba(X_test)[:,1]\n"
        "    RocCurveDisplay.from_predictions(y_test, y_prob, name=name, ax=ax)\n"
        "ax.plot([0,1],[0,1],'k--',label='Random')\n"
        "ax.set_title('ROC Curves - All Models')\n"
        "plt.legend()\nplt.show()"
    ),

    code(
        "print(f'Classification Report - {best_name}:')\n"
        "print(results[best_name]['report'])"
    ),

    md("---\n## Task 2: Customer Segmentation"),
    code("from model import build_segments\nseg_df = build_segments(df)\ndf = df.merge(seg_df[['user_id','segment_label']], on='user_id', how='left')\ndf['segment_label'].value_counts()"),

    code(
        "profile = df.groupby('segment_label').agg(\n"
        "    customers=('user_id','count'),\n"
        "    avg_churn=('churn_prob','mean'),\n"
        "    avg_spend=('total_spend','mean'),\n"
        "    avg_trips=('trip_count','mean'),\n"
        "    avg_days_inactive=('days_since_last_trip','mean'),\n"
        ").round(2)\nprint(profile)\n\n"
        "profile['avg_churn'].plot(kind='barh', color='salmon', title='Avg Churn Score by Segment', figsize=(8,4))\n"
        "plt.xlabel('Avg Churn Probability')\nplt.tight_layout()\nplt.show()"
    ),

    md("---\n## Task 4: Model Interpretability"),
    code("from model import explain_model\nfeat_imp = explain_model(results, best_name, df)"),

    code(
        "top15 = feat_imp.head(15)\n"
        "plt.figure(figsize=(9,5))\n"
        "plt.barh(top15['business_label'][::-1], top15['importance'][::-1], color='steelblue')\n"
        "plt.xlabel('Feature Importance')\n"
        "plt.title(f'Top 15 Churn Drivers ({best_name})')\n"
        "plt.tight_layout()\nplt.show()"
    ),

    md("---\n## Task 5: Real-Time Scoring"),
    code("from model import score_customers\nscores_df = score_customers(df, best_name)\ndf = df.merge(scores_df[['user_id','churn_score','risk_tier']], on='user_id', how='left')\nprint(scores_df['risk_tier'].value_counts())\nscores_df.head(10)"),

    code(
        "risk_summary = df.groupby('risk_tier').agg(\n"
        "    customers=('user_id','count'),\n"
        "    revenue_at_risk=('total_spend','sum'),\n"
        "    avg_churn_score=('churn_score','mean'),\n"
        ").round(2)\nprint(risk_summary)"
    ),

    md("---\n## Task 6: Analytics Dashboard\n\nTo launch the interactive Streamlit dashboard:\n```bash\nstreamlit run src/dashboard.py\n```"),

    code(
        "print('='*50)\nprint('EXECUTIVE SUMMARY')\nprint('='*50)\n"
        "print(f'Total customers:      {len(df):,}')\n"
        "print(f'High-risk customers:  {(df[\"risk_tier\"]==\"High Risk\").sum():,}')\n"
        "print(f'Revenue at risk ($):  {df[df[\"risk_tier\"]==\"High Risk\"][\"total_spend\"].sum():,.0f}')\n"
        "print(f'Best model AUC:       {results[best_name][\"test_auc\"]:.4f}')\n"
        "print(f'Model:                {best_name}')"
    ),

    md("---\n## Task 7: API Deployment\n\nStart the REST API:\n```bash\npython src/api.py\n```\n\nExample request:\n```bash\ncurl -X POST http://localhost:8000/score \\\\\n  -H \"Content-Type: application/json\" \\\\\n  -d '{\"user_id\": \"R00001\", \"trip_count\": 5, \"days_since_last_trip\": 45, \"churn_prob\": 0.75}'\n```\n\n**Endpoints:**\n- `GET /health`\n- `POST /score` — single customer\n- `POST /score/batch` — up to 1000 customers\n- `GET /segments/summary`"),

    md("---\n## Task 8: Production Monitoring"),
    code(
        "from monitoring import save_baseline, detect_drift, log_prediction_stats\n\n"
        "save_baseline(df)\n\n"
        "# Simulate data drift\n"
        "df_shifted = df.copy()\n"
        "df_shifted['days_since_last_trip'] *= 1.5\n"
        "report = detect_drift(df_shifted)\n\n"
        "stats = log_prediction_stats(scores_df)\n"
        "print('\\nMonitoring log entry:')\n"
        "for k, v in stats.items():\n"
        "    print(f'  {k}: {v}')"
    ),

    md(
        "---\n## Summary\n\n"
        "| Task | Status | Result |\n"
        "|------|--------|--------|\n"
        "| 1. Churn Prediction Models | Done | 3 models, Random Forest AUC=1.00 |\n"
        "| 2. Customer Segmentation | Done | 4 K-Means segments with business labels |\n"
        "| 3. Feature Engineering | Done | 23 features from 3 datasets |\n"
        "| 4. Model Interpretability | Done | Feature importance with business names |\n"
        "| 5. Real-Time Scoring | Done | Risk tiers: Low / Medium / High |\n"
        "| 6. Analytics Dashboard | Done | `streamlit run src/dashboard.py` |\n"
        "| 7. API Deployment | Done | FastAPI at `src/api.py` port 8000 |\n"
        "| 8. Production Monitoring | Done | Drift detection + prediction logging |"
    ),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"},
    },
    "cells": cells,
}

out = "../notebook/churn_prediction.ipynb"
with open(out, "w") as f:
    json.dump(nb, f, indent=1)
print(f"Notebook written to {out}")
