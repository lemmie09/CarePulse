import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from utils import PEER_FEATURES_PATH, PROVIDER_SCORES_PATH, inject_css, render_top_nav, hero, metric_card, load_data, load_aspect_data

st.set_page_config(page_title="Find the One for You", page_icon="C", layout="wide")
inject_css()
render_top_nav("Find the One for You")

peer_path = PEER_FEATURES_PATH
if not peer_path.exists():
    st.error("provider_peer_features.csv not found. Run the peer feature script first.")
    st.stop()

df = pd.read_csv(peer_path)
reviews_df = load_aspect_data()
_, biz_df = load_data()

CARE_NEEDS = {
    "General check-up / family doctor": ["family medicine", "family practice", "primary care", "internal medicine", "general practitioner", "clinic"],
    "Dental care": ["dentist", "dental", "orthodont", "oral surgeon", "periodont", "endodont", "dds", "dmd"],
    "Urgent care": ["urgent care", "walk-in clinic", "emergency", "medical center"],
    "Women’s health": ["obstetrics", "gynecology", "obgyn", "women's health"],
    "Children / pediatrics": ["pediatric", "children's clinic", "pediatrics"],
    "Mental health support": ["psychiatrist", "psychologist", "mental health", "counseling", "therapy", "therapist"],
    "Vision / eye care": ["optometrist", "ophthalmologist", "eye care", "vision"],
    "Bones / joints / orthopedic": ["orthopedic", "sports medicine", "spine", "joint", "pain management", "chiropractic", "chiropractor"],
    "Skin care / dermatology": ["dermatology", "dermatologist", "skin care clinic"],
}

HEALTHCARE_TERMS = [
    "doctor", "doctors", "physician", "clinic", "medical", "medicine", "hospital", "dentist", "dental",
    "orthodont", "oral surgeon", "optometrist", "ophthalmologist", "urgent care", "family medicine",
    "internal medicine", "pediatric", "pediatrics", "psychiatrist", "psychologist", "therapy", "therapist",
    "mental health", "obgyn", "gynecology", "obstetrics", "dermatology", "dermatologist", "orthopedic",
    "chiropractic", "chiropractor", "rehab", "rehabilitation", "wellness center", "healthcare", "health care",
    "pain management", "medical center", "eye care", "vision", "primary care", "surgeon", "specialist",
    "dds", "dmd"
]

NON_HEALTHCARE_EXCLUSIONS = [
    "restaurant", "bar", "bbq", "barbacoa", "spa", "salon", "fitness", "gym", "cafe", "coffee", "bakery",
    "grill", "tacos", "burger", "food", "eatery", "market", "brew", "brewery", "pub", "hotel", "travel",
    "auto", "car wash", "home cleaning", "pet", "dog", "cat", "massage spa"
]

hero(
    "Find the right provider for your needs",
    "This care-fit engine ranks providers using peer percentile, evidence strength, patient sentiment, provider quality, and aspect-level experience signals."
)

st.markdown(
"""
<style>
.provider-card {
    background: rgba(255,255,255,0.97);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 24px;
    padding: 20px;
    box-shadow: 0 12px 28px rgba(15,23,42,0.05);
    margin-bottom: 16px;
}
.provider-name {
    font-size: 1.32rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}
.provider-sub {
    font-size: 0.96rem;
    color: #64748b;
    margin-bottom: 10px;
}
.trust-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.8rem;
    font-weight: 800;
}
.badge-verified { background: #eefbf5; color: #15803d; }
.badge-top { background: #fff7ed; color: #b45309; }
.badge-board { background: #eff6ff; color: #1d4ed8; }
.soft-panel {
    background: #f8fafc;
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 18px;
    padding: 14px;
    height: 100%;
}
.metric-kicker {
    font-size: 0.82rem;
    color: #64748b;
    font-weight: 700;
    margin-bottom: 6px;
}
.metric-main {
    font-size: 1.85rem;
    color: #0f172a;
    font-weight: 850;
    line-height: 1;
    margin-bottom: 8px;
}
.metric-sub {
    font-size: 0.9rem;
    color: #475569;
}
.score-chip {
    display: inline-block;
    background: #fff;
    border: 1px solid rgba(148,163,184,0.18);
    padding: 8px 12px;
    border-radius: 14px;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: #334155;
    font-weight: 700;
}
.review-tag-positive {
    display: inline-block;
    background: #ecfeff;
    color: #155e75;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-right: 8px;
    margin-bottom: 8px;
}
.review-tag-concern {
    display: inline-block;
    background: #fff7ed;
    color: #9a3412;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-right: 8px;
    margin-bottom: 8px;
}
.concierge-strip {
    border-left: 5px solid #0f766e;
    background: #f8fafc;
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 12px;
    color: #334155;
    font-size: 0.96rem;
    line-height: 1.6;
}
.section-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    margin-top: 6px;
    margin-bottom: 10px;
}
.compare-card {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.05);
    min-height: 420px;
}
.compare-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}
.compare-sub {
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 12px;
}
.compare-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(148,163,184,0.12);
    font-size: 0.92rem;
    color: #334155;
}
.compare-row:last-child {
    border-bottom: none;
}
.compare-label {
    color: #64748b;
    font-weight: 700;
}
.compare-value {
    color: #0f172a;
    font-weight: 800;
    text-align: right;
}
.small-note {
    font-size: 0.92rem;
    color: #334155;
    line-height: 1.55;
    margin-top: 12px;
}
.snippet-box {
    background: #ffffff;
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 16px;
    padding: 12px;
    font-size: 0.93rem;
    color: #334155;
    line-height: 1.55;
    margin-bottom: 10px;
}
.snippet-label-pos {
    font-size: 0.78rem;
    font-weight: 800;
    color: #0f766e;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.snippet-label-neg {
    font-size: 0.78rem;
    font-weight: 800;
    color: #b45309;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
</style>
""",
    unsafe_allow_html=True
)

categories_df = (
    biz_df[["name", "categories"]]
    .dropna(subset=["name"])
    .groupby("name", as_index=False)["categories"]
    .agg(lambda s: " | ".join(sorted(set([str(x) for x in s if pd.notna(x)]))))
    .rename(columns={"name": "business_name"})
)

df = df.merge(categories_df, on="business_name", how="left")

def is_healthcare_provider(cat_text: str) -> bool:
    text = str(cat_text).lower()
    has_healthcare = any(term in text for term in HEALTHCARE_TERMS)
    has_exclusion = any(term in text for term in NON_HEALTHCARE_EXCLUSIONS)
    return has_healthcare and not has_exclusion

df["is_healthcare_provider"] = df["categories"].fillna("").apply(is_healthcare_provider)
df = df[df["is_healthcare_provider"] == True].copy()

c1, c2, c3 = st.columns([1.25, 1, 1])
with c1:
    selected_need = st.selectbox("Care need", list(CARE_NEEDS.keys()))
with c2:
    selected_state = st.selectbox("Preferred state", ["All"] + sorted(df["state"].dropna().unique().tolist()))
with c3:
    priority = st.selectbox(
        "Priority",
        [
            "Overall quality",
            "Better communication",
            "Better staff experience",
            "Lower wait-time concerns",
            "Better cleanliness",
            "Lower billing concerns"
        ]
    )

need_terms = CARE_NEEDS[selected_need]
df["need_match"] = df["categories"].fillna("").str.lower().apply(
    lambda x: int(any(term in x for term in need_terms))
)

rec_df = df[df["need_match"] == 1].copy()
if selected_state != "All":
    rec_df = rec_df[rec_df["state"] == selected_state].copy()

if rec_df.empty:
    st.warning("No providers matched the selected care need and location.")
    st.stop()

def norm(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-9)

rec_df["stars_norm2"] = norm(rec_df["avg_stars"])
rec_df["volume_norm2"] = norm(rec_df["total_reviews"])
rec_df["sent_norm2"] = rec_df["positive_review_ratio"] / 100.0
rec_df["doctor_quality"] = rec_df["doctor_care_score"]
rec_df["staff_quality"] = rec_df["staff_behavior_score"]
rec_df["communication_quality"] = rec_df["communication_score"]
rec_df["cleanliness_quality"] = rec_df["cleanliness_facility_score"]
rec_df["wait_concern"] = rec_df["wait_time_score"].clip(lower=0)
rec_df["billing_concern"] = rec_df["billing_cost_score"].clip(lower=0)

if priority == "Better communication":
    rec_df["match_score"] = (
        0.20 * rec_df["sent_norm2"] +
        0.16 * rec_df["stars_norm2"] +
        0.10 * rec_df["volume_norm2"] +
        0.22 * rec_df["communication_quality"] +
        0.08 * rec_df["staff_quality"] +
        0.08 * rec_df["doctor_quality"] +
        0.16 * (rec_df["recommendation_percentile"] / 100.0)
    )
elif priority == "Better staff experience":
    rec_df["match_score"] = (
        0.20 * rec_df["sent_norm2"] +
        0.16 * rec_df["stars_norm2"] +
        0.10 * rec_df["volume_norm2"] +
        0.22 * rec_df["staff_quality"] +
        0.08 * rec_df["communication_quality"] +
        0.08 * rec_df["doctor_quality"] +
        0.16 * (rec_df["recommendation_percentile"] / 100.0)
    )
elif priority == "Lower wait-time concerns":
    rec_df["match_score"] = (
        0.20 * rec_df["sent_norm2"] +
        0.16 * rec_df["stars_norm2"] +
        0.10 * rec_df["volume_norm2"] +
        0.10 * rec_df["doctor_quality"] +
        0.08 * rec_df["communication_quality"] -
        0.20 * rec_df["wait_concern"] +
        0.16 * (rec_df["recommendation_percentile"] / 100.0)
    )
elif priority == "Better cleanliness":
    rec_df["match_score"] = (
        0.20 * rec_df["sent_norm2"] +
        0.16 * rec_df["stars_norm2"] +
        0.10 * rec_df["volume_norm2"] +
        0.22 * rec_df["cleanliness_quality"] +
        0.08 * rec_df["staff_quality"] +
        0.08 * rec_df["doctor_quality"] +
        0.16 * (rec_df["recommendation_percentile"] / 100.0)
    )
elif priority == "Lower billing concerns":
    rec_df["match_score"] = (
        0.20 * rec_df["sent_norm2"] +
        0.16 * rec_df["stars_norm2"] +
        0.10 * rec_df["volume_norm2"] +
        0.10 * rec_df["doctor_quality"] +
        0.08 * rec_df["communication_quality"] -
        0.20 * rec_df["billing_concern"] +
        0.16 * (rec_df["recommendation_percentile"] / 100.0)
    )
else:
    rec_df["match_score"] = (
        0.20 * rec_df["sent_norm2"] +
        0.18 * rec_df["stars_norm2"] +
        0.10 * rec_df["volume_norm2"] +
        0.10 * rec_df["doctor_quality"] +
        0.08 * rec_df["staff_quality"] +
        0.06 * rec_df["communication_quality"] +
        0.06 * rec_df["cleanliness_quality"] +
        0.22 * (rec_df["recommendation_percentile"] / 100.0)
    )

rec_df["match_score"] = (rec_df["match_score"] * 100).round(2)
rec_df = rec_df.sort_values(["match_score", "recommendation_score", "total_reviews"], ascending=[False, False, False])
rec_df = rec_df.drop_duplicates(subset=["business_name", "city", "state"])

peer_avg = {
    "doctor": rec_df["doctor_care_score"].mean(),
    "communication": rec_df["communication_score"].mean(),
    "staff": rec_df["staff_behavior_score"].mean(),
    "wait": rec_df["wait_time_score"].mean(),
    "billing": rec_df["billing_cost_score"].mean(),
}

def trust_badges(row):
    badges = []
    if row["evidence_strength"] == "High":
        badges.append(("Verified review depth", "verified"))
    if row["positive_review_ratio"] >= 85:
        badges.append(("Strong patient sentiment", "board"))
    if row["recommendation_percentile"] >= 99:
        badges.append(("Top 1% provider fit", "top"))
    elif row["recommendation_percentile"] >= 90:
        badges.append(("Top 10% provider fit", "top"))
    return badges

def sub_scores(row):
    return {
        "Doctor care": round(max(row["doctor_care_score"], 0) * 100, 1),
        "Communication": round(max(row["communication_score"], 0) * 100, 1),
        "Staff experience": round(max(row["staff_behavior_score"], 0) * 100, 1),
        "Wait-time concern": round(max(row["wait_concern"], 0) * 100, 1),
        "Billing concern": round(max(row["billing_concern"], 0) * 100, 1),
    }

def positive_tags(row):
    tags = []
    if row["doctor_care_score"] > peer_avg["doctor"]:
        tags.append("Thorough")
    if row["communication_score"] > peer_avg["communication"]:
        tags.append("Explains well")
    if row["staff_behavior_score"] > peer_avg["staff"]:
        tags.append("Friendly staff")
    if row["cleanliness_facility_score"] > 0.10:
        tags.append("Clean facility")
    if row["positive_review_ratio"] > 85:
        tags.append("Would return")
    return tags[:5]

def concern_tags(row):
    tags = []
    if row["wait_concern"] > peer_avg["wait"]:
        tags.append("Long wait")
    if row["billing_concern"] > peer_avg["billing"]:
        tags.append("Billing issues")
    return tags[:3]

def rationale(row):
    strengths = []
    concerns = []

    if row["communication_vs_peer"] > 0:
        strengths.append("strong communication")
    if row["doctor_vs_peer"] > 0:
        strengths.append("better doctor care")
    if row["staff_vs_peer"] > 0:
        strengths.append("good staff experience")
    if row["wait_vs_peer"] < 0:
        strengths.append("lower wait-time concern")
    if row["billing_vs_peer"] < 0:
        strengths.append("lower billing concern")

    if row["wait_vs_peer"] > 0:
        concerns.append("wait time may be a concern")
    if row["billing_vs_peer"] > 0:
        concerns.append("billing concerns appear more often")
    if row["communication_vs_peer"] < 0:
        concerns.append("communication is weaker than peers")

    strength_text = ", ".join(strengths[:2]) if strengths else "balanced overall signals"
    concern_text = concerns[0] if concerns else "no major concern stands out"

    if row["evidence_strength"] == "High":
        evidence_text = "high review confidence"
    elif row["evidence_strength"] == "Medium":
        evidence_text = "moderate review confidence"
    else:
        evidence_text = "limited review confidence"

    templates = [
        f"{strength_text.capitalize()}. {concern_text.capitalize()}. {evidence_text.capitalize()}.",
        f"Stands out for {strength_text}. Main watchout: {concern_text}. {evidence_text.capitalize()}.",
        f"Good fit because of {strength_text}. Possible tradeoff: {concern_text}. {evidence_text.capitalize()}."
    ]

    idx = int(abs(hash(str(row['business_name']))) % len(templates))
    return templates[idx]

def verdict(row):
    if row["match_score"] >= 80:
        return "Strong overall fit"
    if row["match_score"] >= 65:
        return "Good fit with some tradeoffs"
    return "Consider as a secondary option"

def shorten(text, n=220):
    text = str(text).strip().replace("\n", " ")
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0] + "..."

def get_review_snippets(provider_name):
    provider_reviews = reviews_df[reviews_df["business_name"] == provider_name].copy()

    pos_snippet = None
    neg_snippet = None

    if not provider_reviews.empty:
        pos_reviews = provider_reviews[provider_reviews["sentiment"] == "positive"].copy()
        neg_reviews = provider_reviews[provider_reviews["sentiment"] == "negative"].copy()

        if not pos_reviews.empty:
            pos_reviews["signal_strength"] = (
                pos_reviews.get("aspect_doctor_care", 0).fillna(0) +
                pos_reviews.get("aspect_staff_behavior", 0).fillna(0) +
                pos_reviews.get("aspect_communication", 0).fillna(0) +
                pos_reviews.get("aspect_cleanliness_facility", 0).fillna(0)
            )
            pos_reviews = pos_reviews.sort_values(["signal_strength", "stars"], ascending=[False, False])
            pos_snippet = shorten(pos_reviews.iloc[0]["text_clean"])

        if not neg_reviews.empty:
            neg_reviews["signal_strength"] = (
                neg_reviews.get("aspect_wait_time", 0).fillna(0) +
                neg_reviews.get("aspect_billing_cost", 0).fillna(0) +
                neg_reviews.get("aspect_staff_behavior", 0).fillna(0)
            )
            neg_reviews = neg_reviews.sort_values(["signal_strength", "stars"], ascending=[False, True])
            neg_snippet = shorten(neg_reviews.iloc[0]["text_clean"])

    return pos_snippet, neg_snippet

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Matched Providers", f"{len(rec_df):,}", "Strict healthcare eligibility")
with m2:
    metric_card("Care Need", selected_need, "Recommendation context")
with m3:
    metric_card("Priority", priority, "Ranking preference")
with m4:
    metric_card("Model Layer", "Care-Fit Engine", "Peer comparison + evidence strength")

st.markdown("---")




st.markdown("""
<style>
div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    border-radius: 20px !important;
    box-shadow: 0 14px 30px rgba(15,23,42,0.08) !important;
}

[data-testid="stMetric"] {
    background: #f8fafc;
    border-radius: 14px;
    padding: 10px 12px;
}

[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: #64748b !important;
    font-weight: 800 !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.45rem !important;
    color: #0f172a !important;
    font-weight: 900 !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Cleaner recommendation container cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.97) !important;
    border: 1px solid rgba(203,213,225,0.95) !important;
    border-radius: 22px !important;
    box-shadow: 0 18px 38px rgba(15,23,42,0.10) !important;
}

/* Keep metric boxes soft but readable */
[data-testid="stMetric"] {
    background: #f8fafc !important;
    border: 1px solid rgba(226,232,240,0.95) !important;
    border-radius: 16px !important;
    padding: 12px 14px !important;
}

/* Recommendation info banner */
div[data-testid="stAlert"] {
    background: rgba(255,255,255,0.94) !important;
    border: 1px solid rgba(203,213,225,0.8) !important;
    border-radius: 16px !important;
    color: #334155 !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Strong readable recommendation cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(203,213,225,0.95) !important;
    border-radius: 22px !important;
    box-shadow: 0 18px 40px rgba(15,23,42,0.12) !important;
    padding: 18px !important;
}

/* Inner card content */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: transparent !important;
}

/* Metric boxes */
[data-testid="stMetric"] {
    background: rgba(248,250,252,0.98) !important;
    border: 1px solid rgba(226,232,240,1) !important;
    border-radius: 16px !important;
    padding: 12px 14px !important;
}

/* Make text stronger */
div[data-testid="stVerticalBlockBorderWrapper"] h3,
div[data-testid="stVerticalBlockBorderWrapper"] p,
div[data-testid="stVerticalBlockBorderWrapper"] span {
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)




st.markdown("""
<style>
/* Recommendation cards: soft teal theme */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(135deg, rgba(236,253,245,0.98), rgba(240,253,250,0.96)) !important;
    border: 1px solid rgba(15,118,110,0.28) !important;
    border-radius: 22px !important;
    box-shadow: 0 16px 34px rgba(15,118,110,0.12) !important;
}

/* Metric cards inside recommendation boxes */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(15,118,110,0.18) !important;
    border-radius: 16px !important;
    padding: 12px 14px !important;
}

/* Match score box */
div[data-testid="stVerticalBlockBorderWrapper"] button {
    background: #0f766e !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Darker recommendation card panels */
section.main div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(135deg, #dff3ef 0%, #e8f7f4 100%) !important;
    border: 1.5px solid rgba(15,118,110,0.35) !important;
    border-radius: 22px !important;
    box-shadow: 0 18px 36px rgba(15,118,110,0.16) !important;
}

/* Metric boxes inside recommendation cards */
section.main div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.94) !important;
    border: 1px solid rgba(15,118,110,0.24) !important;
    border-radius: 16px !important;
}

/* Match score card on right */
section.main div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMetric"]:has(div[data-testid="stMetricLabel"]) {
    box-shadow: 0 8px 18px rgba(15,118,110,0.08) !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("## Top recommendations")
st.info("Ranked using patient sentiment, review depth, care-specific aspect signals, and peer comparison.")

top_recs = rec_df.head(3).copy()

def safe_num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default

def pct_value(row, *cols):
    for col in cols:
        if col in row and pd.notna(row[col]):
            value = safe_num(row[col])
            return round(value * 100, 1) if value <= 1 else round(value, 1)
    return 0.0

def match_label(score):
    score = safe_num(score)
    if score >= 75:
        return "Excellent Match"
    if score >= 60:
        return "Good Match"
    if score >= 45:
        return "Fair Match"
    return "Emerging Match"

def top_strengths(row):
    signals = {
        "Doctor care": pct_value(row, "doctor_quality", "doctor_care_score"),
        "Communication": pct_value(row, "communication_quality", "communication_score"),
        "Staff experience": pct_value(row, "staff_quality", "staff_behavior_score"),
        "Clean facility": pct_value(row, "cleanliness_quality", "cleanliness_facility_score"),
    }
    ranked = sorted(signals.items(), key=lambda x: x[1], reverse=True)
    return [name for name, value in ranked[:2] if value > 0] or ["Balanced feedback"]

def main_watchout(row):
    wait = pct_value(row, "wait_concern", "wait_time_score")
    billing = pct_value(row, "billing_concern", "billing_cost_score")
    if wait >= billing and wait > 20:
        return "Wait time"
    if billing > wait and billing > 12:
        return "Billing"
    return "No major concern"

for idx, (_, row) in enumerate(top_recs.iterrows(), start=1):
    name = row.get("business_name", "")
    city = row.get("city", "")
    state = row.get("state", "")

    score = round(safe_num(row.get("match_score", row.get("recommendation_score", 0))), 2)
    percentile = round(safe_num(row.get("recommendation_percentile", 0)), 1)
    stars = round(safe_num(row.get("avg_stars", 0)), 2)
    reviews = int(safe_num(row.get("total_reviews", 0)))
    positive = pct_value(row, "positive_review_ratio", "positive_review_pct")
    evidence = row.get("evidence_strength", "N/A")
    strengths = ", ".join(top_strengths(row))
    watchout = main_watchout(row)
    label = match_label(score)

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #d4f2ed 0%, #e0f7f3 50%, #c7ebe5 100%);
        border: 1.8px solid rgba(15,118,110,0.42);
        border-radius: 24px;
        padding: 26px 28px;
        margin-bottom: 10px;
        box-shadow: 0 18px 40px rgba(15,118,110,0.18);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    ">
        <div style="display:grid; grid-template-columns: 1fr 240px; gap:28px; align-items:center;">
            <div>
                <div style="font-size:13px; color:#0f766e; font-weight:900; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:18px;">
                    Recommendation {idx}
                </div>

                <div style="font-size:31px; line-height:1.15; font-weight:950; color:#0f172a; margin-bottom:12px;">
                    {name}
                </div>

                <div style="font-size:16px; color:#475569; margin-bottom:24px;">
                    {city}, {state}
                </div>

                <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; margin-bottom:22px;">
                    <div style="background:rgba(255,255,255,0.82); border:1px solid rgba(15,118,110,0.22); border-radius:16px; padding:14px 16px;">
                        <div style="font-size:13px; color:#64748b; font-weight:800;">Stars</div>
                        <div style="font-size:24px; color:#0f172a; font-weight:950;">{stars}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.82); border:1px solid rgba(15,118,110,0.22); border-radius:16px; padding:14px 16px;">
                        <div style="font-size:13px; color:#64748b; font-weight:800;">Reviews</div>
                        <div style="font-size:24px; color:#0f172a; font-weight:950;">{reviews}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.82); border:1px solid rgba(15,118,110,0.22); border-radius:16px; padding:14px 16px;">
                        <div style="font-size:13px; color:#64748b; font-weight:800;">Positive</div>
                        <div style="font-size:24px; color:#0f172a; font-weight:950;">{positive}%</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.82); border:1px solid rgba(15,118,110,0.22); border-radius:16px; padding:14px 16px;">
                        <div style="font-size:13px; color:#64748b; font-weight:800;">Peer rank</div>
                        <div style="font-size:24px; color:#0f172a; font-weight:950;">{percentile}</div>
                    </div>
                </div>

                <div style="font-size:16px; color:#0f172a; line-height:1.8;">
                    <b>Evidence strength:</b> {evidence}<br>
                    <b>Best strengths:</b> {strengths}<br>
                    <b>Main watchout:</b> {watchout}
                </div>
            </div>

            <div style="
                background: linear-gradient(180deg, #0f766e 0%, #115e59 100%);
                color:white;
                border-radius:22px;
                padding:26px 22px;
                text-align:center;
                box-shadow:0 16px 32px rgba(15,118,110,0.28);
            ">
                <div style="font-size:15px; opacity:0.88; font-weight:800; margin-bottom:8px;">
                    {label}
                </div>
                <div style="font-size:42px; font-weight:950; line-height:1;">
                    {score}
                </div>
                <div style="font-size:13px; opacity:0.82; margin-top:9px;">
                    Care-fit score
                </div>
            </div>
        </div>
    </div>
    """

    components.html(card_html, height=310)

    if st.button("View Details", key=f"top_rec_dark_card_{idx}_{name}"):
        st.session_state["selected_provider"] = name
        st.switch_page("pages/1_Provider_Analysis.py")

st.markdown("---")
st.markdown("## Compare providers")

compare_options = rec_df["business_name"].dropna().head(15).tolist()
default_compare = compare_options[:3] if len(compare_options) >= 3 else compare_options

selected_compare = st.multiselect(
    "Select up to 3 providers to compare",
    options=compare_options,
    default=default_compare,
    max_selections=3
)

def safe_num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default

def pct_from_ratio(value):
    value = safe_num(value)
    if value <= 1:
        return round(value * 100, 1)
    return round(value, 1)

def compact_best(row):
    signals = {
        "Doctor care": pct_from_ratio(row.get("doctor_quality", row.get("doctor_care_score", 0))),
        "Communication": pct_from_ratio(row.get("communication_quality", row.get("communication_score", 0))),
        "Staff": pct_from_ratio(row.get("staff_quality", row.get("staff_behavior_score", 0))),
        "Cleanliness": pct_from_ratio(row.get("cleanliness_quality", row.get("cleanliness_facility_score", 0))),
    }
    best = max(signals, key=signals.get)
    return best if signals[best] > 0 else "Balanced"

def compact_watch(row):
    wait = pct_from_ratio(row.get("wait_concern", row.get("wait_time_score", 0)))
    billing = pct_from_ratio(row.get("billing_concern", row.get("billing_cost_score", 0)))
    if wait >= billing and wait > 10:
        return "Wait time"
    if billing > wait and billing > 10:
        return "Billing"
    return "Low concern"

if selected_compare:
    compare_df = rec_df[rec_df["business_name"].isin(selected_compare)].copy()

    summary_rows = []
    for _, row in compare_df.iterrows():
        summary_rows.append({
            "Provider": row.get("business_name", ""),
            "Location": f"{row.get('city', '')}, {row.get('state', '')}",
            "Care-Fit": round(safe_num(row.get("match_score", row.get("recommendation_score", 0))), 2),
            "Stars": round(safe_num(row.get("avg_stars", 0)), 2),
            "Reviews": int(safe_num(row.get("total_reviews", 0))),
            "Positive %": pct_from_ratio(row.get("positive_review_ratio", row.get("positive_review_pct", 0))),
            "Best For": compact_best(row),
            "Watch": compact_watch(row),
        })

    summary_df = pd.DataFrame(summary_rows)

    st.markdown(
        """
        <div style="background:rgba(255,255,255,0.88); border:1px solid rgba(148,163,184,0.16); border-radius:18px; padding:15px 18px; margin-bottom:18px; color:#334155; line-height:1.55;">
            Compare providers using care-fit score, patient sentiment, review volume, and care-specific signals. This view is designed to support quick decision-making instead of reading many reviews manually.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("### Care signal comparison")

    radar_rows = []
    for _, row in compare_df.iterrows():
        provider = row.get("business_name", "")
        radar_rows.extend([
            {"Provider": provider, "Signal": "Doctor care", "Score": pct_from_ratio(row.get("doctor_quality", row.get("doctor_care_score", 0)))},
            {"Provider": provider, "Signal": "Communication", "Score": pct_from_ratio(row.get("communication_quality", row.get("communication_score", 0)))},
            {"Provider": provider, "Signal": "Staff", "Score": pct_from_ratio(row.get("staff_quality", row.get("staff_behavior_score", 0)))},
            {"Provider": provider, "Signal": "Low wait concern", "Score": max(0, 100 - pct_from_ratio(row.get("wait_concern", row.get("wait_time_score", 0))))},
            {"Provider": provider, "Signal": "Low billing concern", "Score": max(0, 100 - pct_from_ratio(row.get("billing_concern", row.get("billing_cost_score", 0))))},
        ])

    radar_df = pd.DataFrame(radar_rows)

    fig_compare = px.line_polar(
        radar_df,
        r="Score",
        theta="Signal",
        color="Provider",
        line_close=True,
        range_r=[0, 100],
        title="Provider Strength Profile"
    )
    fig_compare.update_traces(fill="toself")
    fig_compare.update_layout(height=520)
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("### Quick decision cards")

    cols = st.columns(len(compare_df))
    for col, (_, row) in zip(cols, compare_df.iterrows()):
        with col:
            provider = row.get("business_name", "")
            city = row.get("city", "")
            state = row.get("state", "")
            care = round(safe_num(row.get("match_score", row.get("recommendation_score", 0))), 2)
            stars = round(safe_num(row.get("avg_stars", 0)), 2)
            reviews = int(safe_num(row.get("total_reviews", 0)))
            positive = pct_from_ratio(row.get("positive_review_ratio", row.get("positive_review_pct", 0)))
            best = compact_best(row)
            watch = compact_watch(row)

            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.90); border:1px solid rgba(148,163,184,0.16); border-radius:20px; padding:18px; box-shadow:0 10px 24px rgba(15,23,42,0.05); min-height:260px;">
                    <div style="font-size:0.78rem; color:#0f766e; font-weight:900; text-transform:uppercase; letter-spacing:0.05em;">Decision card</div>
                    <div style="font-size:1.05rem; font-weight:900; color:#0f172a; margin-top:8px; line-height:1.25;">{provider}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-top:4px;">{city}, {state}</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:14px;">
                        <div style="background:#f8fafc; border-radius:14px; padding:10px;"><b>Care-Fit</b><br>{care}</div>
                        <div style="background:#f8fafc; border-radius:14px; padding:10px;"><b>Stars</b><br>{stars}</div>
                        <div style="background:#f8fafc; border-radius:14px; padding:10px;"><b>Reviews</b><br>{reviews}</div>
                        <div style="background:#f8fafc; border-radius:14px; padding:10px;"><b>Positive</b><br>{positive}%</div>
                    </div>
                    <div style="margin-top:14px; padding:12px; border-left:4px solid #0f766e; background:#f8fafc; border-radius:12px; color:#334155;">
                        <b>Best for:</b> {best}<br>
                        <b>Watch:</b> {watch}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("Select providers to compare.")

st.markdown("---")
st.caption("Results are restricted to healthcare providers using a strict eligibility filter, then ranked using peer percentile, evidence strength, sentiment, provider quality, and aspect-level experience signals.")
