import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from utils import inject_css, render_top_nav, hero, metric_card, load_aspect_data, load_data, calculate_cqi, quality_badge, quality_label

st.set_page_config(page_title="Find the One for You", page_icon="🧭", layout="wide")
inject_css()
render_top_nav("Find the One for You")

reviews_df = load_aspect_data()
_, biz_df = load_data()

CARE_NEEDS = {
    "General check-up / family doctor": ["family", "primary", "general", "internal medicine", "family medicine"],
    "Dental care": ["dentist", "dental", "orthodont", "oral"],
    "Urgent care": ["urgent care", "walk-in", "emergency"],
    "Women’s health": ["obstetrics", "gynecology", "women"],
    "Children / pediatrics": ["pediatric", "children"],
    "Mental health support": ["psychiatrist", "counseling", "therapist", "mental health", "psychology"],
    "Vision / eye care": ["optometrist", "ophthalmologist", "vision", "eye"],
    "Bones / joints / orthopedic": ["orthopedic", "sports medicine", "spine", "joint"],
    "Skin care / dermatology": ["dermatology", "skin"],
}

hero(
    "Find the One for You",
    "Discover providers based on your care need, preferred location, and quality signals such as review sentiment, wait-time mentions, communication, and overall provider confidence."
)

c1, c2, c3 = st.columns([1.2, 1, 1])

with c1:
    selected_need = st.selectbox("What kind of care are you looking for?", list(CARE_NEEDS.keys()))
with c2:
    selected_state = st.selectbox("Preferred state", ["All"] + sorted(reviews_df["state"].dropna().unique().tolist()))
with c3:
    priority = st.selectbox("What matters most to you?", [
        "Overall quality",
        "Communication",
        "Lower wait-time concerns",
        "Better staff experience",
        "Better cleanliness"
    ])

provider_summary = (
    reviews_df.groupby(["business_name", "city", "state"])
    .agg(total_reviews=("review_id", "count"), avg_stars=("stars", "mean"))
    .reset_index()
)

cqi_df = (
    reviews_df.groupby("business_name")
    .apply(calculate_cqi)
    .reset_index(name="cqi_tuple")
)
cqi_df["cqi"] = cqi_df["cqi_tuple"].apply(lambda x: x[0])
cqi_df = cqi_df.drop(columns=["cqi_tuple"])

provider_summary = provider_summary.merge(cqi_df, on="business_name", how="left")
provider_summary["quality_band"] = provider_summary["cqi"].apply(quality_label)

aspect_rollup = (
    reviews_df.groupby("business_name")[[
        "aspect_doctor_care",
        "aspect_staff_behavior",
        "aspect_billing_cost",
        "aspect_wait_time",
        "aspect_communication",
        "aspect_cleanliness_facility"
    ]]
    .mean()
    .reset_index()
)

provider_summary = provider_summary.merge(aspect_rollup, on="business_name", how="left")
provider_summary = provider_summary.merge(
    biz_df[["business_id", "name", "categories"]].rename(columns={"name": "business_name"}),
    on="business_name",
    how="left"
)

keywords = CARE_NEEDS[selected_need]
matches = provider_summary["categories"].fillna("").str.lower().apply(
    lambda x: any(k in x for k in keywords)
)
rec_df = provider_summary[matches].copy()

if selected_state != "All":
    rec_df = rec_df[rec_df["state"] == selected_state].copy()

if priority == "Communication":
    rec_df = rec_df.sort_values(["aspect_communication", "cqi", "total_reviews"], ascending=[False, False, False])
elif priority == "Lower wait-time concerns":
    rec_df = rec_df.sort_values(["aspect_wait_time", "cqi"], ascending=[True, False])
elif priority == "Better staff experience":
    rec_df = rec_df.sort_values(["aspect_staff_behavior", "cqi"], ascending=[False, False])
elif priority == "Better cleanliness":
    rec_df = rec_df.sort_values(["aspect_cleanliness_facility", "cqi"], ascending=[False, False])
else:
    rec_df = rec_df.sort_values(["cqi", "total_reviews"], ascending=[False, False])

r1, r2, r3 = st.columns(3)
with r1:
    metric_card("Matched Providers", f"{len(rec_df):,}", "Providers matching your selected care need")
with r2:
    metric_card("Top Need", selected_need, "Current care discovery focus")
with r3:
    metric_card("Priority", priority, "Current decision preference")

st.markdown("## Recommended providers")

top_recs = rec_df.head(9)

if top_recs.empty:
    st.warning("No providers matched the current filters.")
else:
    rows = [top_recs.iloc[i:i+3] for i in range(0, len(top_recs), 3)]
    for row_df in rows:
        cols = st.columns(len(row_df))
        for col, (_, row) in zip(cols, row_df.iterrows()):
            with col:
                wait_score = round((1 - row.get("aspect_wait_time", 0)) * 100, 1)
                comm_score = round(row.get("aspect_communication", 0) * 100, 1)
                clean_score = round(row.get("aspect_cleanliness_facility", 0) * 100, 1)

                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.95); border:1px solid rgba(148,163,184,0.12); border-radius:22px; padding:20px; box-shadow:0 10px 24px rgba(15,23,42,0.05); min-height:270px;">
                        <div style="font-size:1.05rem; font-weight:800; color:#0f172a; margin-bottom:8px;">{row['business_name']}</div>
                        <div style="font-size:0.9rem; color:#64748b; margin-bottom:10px;">{row['city']}, {row['state']}</div>
                        <div style="margin-bottom:10px;">{quality_badge(row['cqi'])}</div>
                        <div style="font-size:0.95rem; color:#334155; margin-bottom:6px;"><b>CQI:</b> {row['cqi']}</div>
                        <div style="font-size:0.95rem; color:#334155; margin-bottom:6px;"><b>Avg Stars:</b> {round(row['avg_stars'], 2)}</div>
                        <div style="font-size:0.95rem; color:#334155; margin-bottom:6px;"><b>Reviews:</b> {int(row['total_reviews'])}</div>
                        <div style="font-size:0.9rem; color:#475569; margin-top:10px;">
                            <b>Communication signal:</b> {comm_score}%<br/>
                            <b>Cleanliness signal:</b> {clean_score}%<br/>
                            <b>Lower wait concern signal:</b> {wait_score}%
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

st.markdown("---")
st.caption("This finder supports care discovery based on provider category matching, review themes, and composite quality signals. It is not a medical diagnosis tool.")
