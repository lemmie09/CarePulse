import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from utils import PEER_FEATURES_PATH, PROVIDER_SCORES_PATH, inject_css, render_top_nav, hero, metric_card, load_aspect_data, calculate_cqi, quality_badge, quality_label

st.set_page_config(page_title="Provider Details", page_icon="C", layout="wide")
inject_css()
render_top_nav("Provider Details")

aspect_df = load_aspect_data()

provider_names = sorted(aspect_df["business_name"].dropna().unique().tolist())

ASPECT_LABELS = {
    "aspect_doctor_care": "Doctor Care",
    "aspect_staff_behavior": "Staff Behavior",
    "aspect_billing_cost": "Billing / Cost",
    "aspect_wait_time": "Wait Time",
    "aspect_communication": "Communication",
    "aspect_cleanliness_facility": "Cleanliness / Facility",
}

hero(
    "Provider Details",
    "Explore provider quality, patient feedback, aspect-level review signals, and location-aware healthcare intelligence."
)

top_bar_left, top_bar_right = st.columns([2.2, 1])
with top_bar_left:
    default_provider = st.session_state.get("selected_provider", provider_names[0])
selected_provider = st.selectbox(
    "Search provider",
    provider_names,
    index=provider_names.index(default_provider) if default_provider in provider_names else 0
)
with top_bar_right:
    sort_reviews = st.selectbox("Review sort", ["Newest first", "Highest stars", "Lowest stars"])

provider_df = aspect_df[aspect_df["business_name"] == selected_provider].copy()

provider_city = provider_df["city"].mode()[0] if not provider_df["city"].mode().empty else "N/A"
provider_state = provider_df["state"].mode()[0] if not provider_df["state"].mode().empty else "N/A"
provider_reviews = len(provider_df)
provider_avg_star = round(provider_df["stars"].mean(), 2)
cqi, star_score, sentiment_score, volume_score = calculate_cqi(provider_df)
band = quality_label(cqi)

sentiment_counts = provider_df["sentiment"].value_counts()
positive_count = sentiment_counts.get("positive", 0)
negative_count = sentiment_counts.get("negative", 0)
neutral_count = sentiment_counts.get("neutral", 0)

st.markdown("---")

left, right = st.columns([1.45, 1])

with left:
    st.markdown(f"## {selected_provider}")
    st.markdown(f"**Location:** {provider_city}, {provider_state}")
    st.markdown(quality_badge(cqi), unsafe_allow_html=True)
    st.caption("Composite Quality Index based on rating quality, review sentiment balance, and review volume confidence.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("CQI", cqi, f"Band: {band}")
    with c2:
        metric_card("Average Stars", provider_avg_star, "Observed provider rating")
    with c3:
        metric_card("Total Reviews", f"{provider_reviews:,}", "Provider review volume")
    with c4:
        pos_rate = round((positive_count / provider_reviews) * 100, 1) if provider_reviews else 0
        metric_card("Positive Share", f"{pos_rate}%", "Positive review proportion")

with right:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cqi,
        title={'text': "Quality Meter"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2563eb"},
            'steps': [
                {'range': [0, 55], 'color': "#fee2e2"},
                {'range': [55, 70], 'color': "#ffedd5"},
                {'range': [70, 85], 'color': "#fef9c3"},
                {'range': [85, 100], 'color': "#dcfce7"}
            ]
        }
    ))
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Patient Reviews", "Strengths & Concerns", "Location"])

with tab1:
    st.markdown("### Provider Performance Snapshot")
    l1, l2 = st.columns(2)

    with l1:
        cqi_df = pd.DataFrame({
            "component": ["Star Score", "Sentiment Score", "Volume Score"],
            "score": [star_score, sentiment_score, volume_score]
        })
        fig_cqi = px.bar(
            cqi_df,
            x="component",
            y="score",
            text="score",
            color="component",
            title="CQI Component Breakdown"
        )
        fig_cqi.update_traces(textposition="outside")
        fig_cqi.update_layout(showlegend=False, height=380, yaxis_range=[0, 110])
        st.plotly_chart(fig_cqi, use_container_width=True)

    with l2:
        sent_df = pd.DataFrame({
            "sentiment": ["positive", "negative", "neutral"],
            "count": [positive_count, negative_count, neutral_count]
        })
        sent_df = sent_df[sent_df["count"] > 0]
        fig_sent = px.pie(
            sent_df,
            names="sentiment",
            values="count",
            hole=0.5,
            title="Sentiment Share"
        )
        fig_sent.update_layout(height=380)
        st.plotly_chart(fig_sent, use_container_width=True)

with tab2:
    st.markdown("### Patient Reviews")

    if sort_reviews == "Highest stars":
        filtered_reviews = provider_df.sort_values(["stars", "date"], ascending=[False, False]).head(10)
    elif sort_reviews == "Lowest stars":
        filtered_reviews = provider_df.sort_values(["stars", "date"], ascending=[True, False]).head(10)
    else:
        filtered_reviews = provider_df.sort_values("date", ascending=False).head(10)

    for _, row in filtered_reviews.iterrows():
        full_text = str(row.get("text_clean", ""))
        preview = full_text[:280] + ("..." if len(full_text) > 280 else "")
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.94); border:1px solid rgba(148,163,184,0.12); border-radius:18px; padding:16px; margin-bottom:14px;">
                <div style="font-weight:700; color:#0f172a;">{row.get("stars", "")} stars • {row.get("date", "")}</div>
                <div style="color:#334155; margin-top:8px;">{preview}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab3:
    st.markdown("### Strengths & Concerns Summary")
    aspect_summary = []
    for col, label in ASPECT_LABELS.items():
        count = int(provider_df[col].sum())
        pct = round((count / provider_reviews) * 100, 1) if provider_reviews else 0
        aspect_summary.append({"aspect": label, "count": count, "pct_reviews": pct})

    aspect_summary_df = pd.DataFrame(aspect_summary).sort_values("count", ascending=False)

    fig_aspects = px.bar(
        aspect_summary_df,
        x="count",
        y="aspect",
        orientation="h",
        text="pct_reviews",
        title="Most Mentioned Review Aspects"
    )
    fig_aspects.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_aspects.update_layout(height=420, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_aspects, use_container_width=True)

with tab4:
    st.markdown("### Provider Location")
    map_df = provider_df.dropna(subset=["latitude", "longitude"]).copy()

    if not map_df.empty:
        lat = float(map_df["latitude"].iloc[0])
        lon = float(map_df["longitude"].iloc[0])

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df.head(1),
            get_position='[longitude, latitude]',
            get_fill_color='[37, 99, 235, 180]',
            get_radius=500,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=11,
            pitch=0,
        )

        st.pydeck_chart(
            pdk.Deck(
                map_style="road",
                map_provider="carto",
                initial_view_state=view_state,
                layers=[layer],
                tooltip={
                    "html": f"<b>{selected_provider}</b><br/>{provider_city}, {provider_state}<br/>CQI: {cqi}",
                    "style": {"backgroundColor": "#111827", "color": "white"}
                }
            )
        )
    else:
        st.info("Location data is not available for this provider.")
