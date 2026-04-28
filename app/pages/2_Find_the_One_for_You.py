import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from utils import inject_css, render_top_nav, hero, metric_card, load_data, load_aspect_data

st.set_page_config(page_title="Find the One for You", page_icon="C", layout="wide")
inject_css()
render_top_nav("Find the One for You")

peer_path = Path("data/processed/provider_peer_features.csv")
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
st.markdown("## Top recommendations")

top_recs = rec_df.head(3)
cols = st.columns(3)

for idx, (_, row) in enumerate(top_recs.iterrows()):
    with cols[idx]:
        pos_snippet, neg_snippet = get_review_snippets(row["business_name"])

        st.markdown('<div class="provider-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="provider-name">{row["business_name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="provider-sub">{row["city"]}, {row["state"]}</div>', unsafe_allow_html=True)

        badges_html = ""
        for label, kind in trust_badges(row):
            cls = "badge-verified" if kind == "verified" else "badge-top" if kind == "top" else "badge-board"
            badges_html += f'<span class="trust-badge {cls}">{label}</span>'
        if not badges_html:
            badges_html = '<span class="trust-badge badge-board">Patient-reviewed provider</span>'
        st.markdown(badges_html, unsafe_allow_html=True)

        left, right = st.columns([1, 1])
        with left:
            st.markdown('<div class="soft-panel">', unsafe_allow_html=True)
            st.markdown('<div class="metric-kicker">Care-Fit Score</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-main">{row["match_score"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-sub">Peer percentile: {row["recommendation_percentile"]:.1f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="soft-panel">', unsafe_allow_html=True)
            st.markdown('<div class="metric-kicker">Trust Snapshot</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="metric-sub">Average stars: <b>{row["avg_stars"]:.2f}</b><br/>Positive review ratio: <b>{row["positive_review_ratio"]:.1f}%</b><br/>Evidence strength: <b>{row["evidence_strength"]}</b></div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Multi-dimensional review scores</div>', unsafe_allow_html=True)
        scores = sub_scores(row)
        st.markdown("".join([f'<span class="score-chip">{k}: {v}</span>' for k, v in scores.items()]), unsafe_allow_html=True)

        st.markdown('<div class="section-title">Review tags</div>', unsafe_allow_html=True)
        pos_html = "".join([f'<span class="review-tag-positive">{t}</span>' for t in positive_tags(row)])
        neg_html = "".join([f'<span class="review-tag-concern">{t}</span>' for t in concern_tags(row)])
        if not pos_html:
            pos_html = '<span class="review-tag-positive">Balanced sentiment</span>'
        st.markdown(pos_html + neg_html, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Why it matches</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="concierge-strip">{rationale(row)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Review evidence</div>', unsafe_allow_html=True)
        if pos_snippet:
            st.markdown(
                f'''
                <div class="snippet-box">
                    <div class="snippet-label-pos">Positive highlight</div>
                    “{pos_snippet}”
                </div>
                ''',
                unsafe_allow_html=True
            )
        if neg_snippet:
            st.markdown(
                f'''
                <div class="snippet-box">
                    <div class="snippet-label-neg">Concern highlight</div>
                    “{neg_snippet}”
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("## Compare providers")

compare_options = rec_df["business_name"].head(12).tolist()
default_compare = compare_options[:3] if len(compare_options) >= 3 else compare_options

selected_compare = st.multiselect(
    "Select up to 3 providers to compare",
    options=compare_options,
    default=default_compare,
    max_selections=3
)

if selected_compare:
    compare_df = rec_df[rec_df["business_name"].isin(selected_compare)].copy()
    compare_cols = st.columns(len(compare_df))

    for col, (_, row) in zip(compare_cols, compare_df.iterrows()):
        with col:
            st.markdown('<div class="compare-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="compare-title">{row["business_name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="compare-sub">{row["city"]}, {row["state"]}</div>', unsafe_allow_html=True)

            st.markdown(f'''
            <div class="compare-row"><span class="compare-label">Care-Fit Score</span><span class="compare-value">{row["match_score"]}</span></div>
            <div class="compare-row"><span class="compare-label">Peer Percentile</span><span class="compare-value">{row["recommendation_percentile"]:.1f}</span></div>
            <div class="compare-row"><span class="compare-label">Evidence Strength</span><span class="compare-value">{row["evidence_strength"]}</span></div>
            <div class="compare-row"><span class="compare-label">Average Stars</span><span class="compare-value">{row["avg_stars"]:.2f}</span></div>
            <div class="compare-row"><span class="compare-label">Reviews</span><span class="compare-value">{int(row["total_reviews"])}</span></div>
            <div class="compare-row"><span class="compare-label">Doctor Care</span><span class="compare-value">{max(row["doctor_care_score"], 0) * 100:.1f}</span></div>
            <div class="compare-row"><span class="compare-label">Communication</span><span class="compare-value">{max(row["communication_score"], 0) * 100:.1f}</span></div>
            <div class="compare-row"><span class="compare-label">Staff Experience</span><span class="compare-value">{max(row["staff_behavior_score"], 0) * 100:.1f}</span></div>
            <div class="compare-row"><span class="compare-label">Wait-Time Concern</span><span class="compare-value">{max(row["wait_concern"], 0) * 100:.1f}</span></div>
            <div class="compare-row"><span class="compare-label">Billing Concern</span><span class="compare-value">{max(row["billing_concern"], 0) * 100:.1f}</span></div>
            ''', unsafe_allow_html=True)

            st.markdown(f'<div class="small-note"><b>Verdict:</b> {verdict(row)}<br/><b>Summary:</b> {rationale(row)}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Results are restricted to healthcare providers using a strict eligibility filter, then ranked using peer percentile, evidence strength, sentiment, provider quality, and aspect-level experience signals.")
