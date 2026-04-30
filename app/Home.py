from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium
import pydeck as pdk
from utils import inject_css, render_top_nav, hero, metric_card, load_aspect_data, predict_distilbert_sentiment, calculate_cqi, quality_badge, quality_label

st.set_page_config(page_title="CarePulse", page_icon="C", layout="wide")
inject_css()
render_top_nav("Home")


reviews_df = load_aspect_data()

ASPECT_LABELS = {
    "aspect_doctor_care": "Doctor Care",
    "aspect_staff_behavior": "Staff Behavior",
    "aspect_billing_cost": "Billing / Cost",
    "aspect_wait_time": "Wait Time",
    "aspect_communication": "Communication",
    "aspect_cleanliness_facility": "Cleanliness / Facility",
}

hero(
    "Find healthcare insights that actually help",
    "Explore provider quality, review themes, patient sentiment, and trust signals to make better care decisions with more clarity and confidence."
)

st.markdown("""
<div class="home-section-note">
    <span class="home-mini-label">Healthcare review intelligence</span><br>
    CarePulse turns patient reviews into structured provider insights using sentiment analysis, aspect extraction, quality scoring, and location-based exploration.
</div>
""", unsafe_allow_html=True)

top1, top2 = st.columns([1, 2])

state_options = ["All"] + sorted(reviews_df["state"].dropna().unique().tolist())

with top1:
    selected_state = st.selectbox("Filter by state", state_options, index=0)

with top2:
    pass
    

filtered_df = reviews_df.copy()
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["state"] == selected_state].copy()

provider_count = filtered_df["business_name"].nunique()
review_count = len(filtered_df)
avg_star = round(filtered_df["stars"].mean(), 2)
positive_rate = round((filtered_df["sentiment"].eq("positive").mean()) * 100, 1)

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Providers", f"{provider_count:,}", "Healthcare providers in current view")
with c2:
    metric_card("Reviews", f"{review_count:,}", "Structured healthcare reviews")
with c3:
    metric_card("Average Stars", avg_star, "Average provider rating")
with c4:
    metric_card("Positive Share", f"{positive_rate}%", "Positive review proportion")

st.markdown("---")

st.markdown("## Provider location")

map_provider_df = (
    filtered_df.dropna(subset=["latitude", "longitude"])
    .groupby(["business_name", "city", "state", "latitude", "longitude"])
    .agg(
        total_reviews=("review_id", "count"),
        avg_stars=("stars", "mean")
    )
    .reset_index()
)

map_provider_df["avg_stars"] = map_provider_df["avg_stars"].round(2)

if not map_provider_df.empty:
    map_provider_df = map_provider_df.sort_values(
        ["total_reviews", "avg_stars"],
        ascending=[False, False]
    ).head(300)

    center_lat = map_provider_df["latitude"].mean()
    center_lon = map_provider_df["longitude"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5 if selected_state != "All" else 4,
        tiles="CartoDB positron"
    )

    for _, row in map_provider_df.iterrows():
        popup_html = f"""
        <b>{row['business_name']}</b><br>
        {row['city']}, {row['state']}<br>
        Stars: {row['avg_stars']} | Reviews: {int(row['total_reviews'])}
        """

        radius = min(15, 5 + int(row["total_reviews"]) / 45)

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=radius,
            color="#0f766e",
            fill=True,
            fill_color="#0f766e",
            fill_opacity=0.72,
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=row["business_name"]
        ).add_to(m)

    map_data = st_folium(
        m,
        width=1300,
        height=560,
        returned_objects=["last_object_clicked_tooltip"]
    )

    clicked_provider = None
    if map_data and map_data.get("last_object_clicked_tooltip"):
        clicked_provider = map_data.get("last_object_clicked_tooltip")
        st.session_state["map_selected_provider"] = clicked_provider

    selected_map_provider = st.session_state.get(
        "map_selected_provider",
        map_provider_df.iloc[0]["business_name"]
    )

    selected_rows = map_provider_df[map_provider_df["business_name"] == selected_map_provider]
    if selected_rows.empty:
        selected_row = map_provider_df.iloc[0]
    else:
        selected_row = selected_rows.iloc[0]

    st.markdown("### Selected provider from map")

    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.92); border-radius:18px; padding:16px; margin-bottom:20px; border:1px solid rgba(148,163,184,0.16); box-shadow:0 10px 24px rgba(15,23,42,0.05);">
            <div style="font-weight:900; color:#0f172a; font-size:1.12rem;">{selected_row['business_name']}</div>
            <div style="color:#64748b; font-size:0.95rem; margin-top:5px;">{selected_row['city']}, {selected_row['state']}</div>
            <div style="color:#334155; font-size:0.95rem; margin-top:10px;">
                <b>Stars:</b> {selected_row['avg_stars']} &nbsp; <b>Reviews:</b> {int(selected_row['total_reviews'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("View Selected Provider Details", key=f"selected_map_details_{selected_row['business_name']}"):
        st.session_state["selected_provider"] = selected_row["business_name"]
        st.switch_page("pages/1_Provider_Analysis.py")

    st.markdown("### Top providers in this map view")

    top_location_providers = map_provider_df.head(6)
    card_rows = [top_location_providers.iloc[i:i+3] for i in range(0, len(top_location_providers), 3)]

    for row_df in card_rows:
        cols = st.columns(3)
        for col, (_, row) in zip(cols, row_df.iterrows()):
            with col:
                st.markdown(
                    f"""
                    <div style="background:rgba(255,255,255,0.92); border-radius:18px; padding:16px; margin-bottom:12px; border:1px solid rgba(148,163,184,0.16); box-shadow:0 8px 18px rgba(15,23,42,0.04); min-height:135px;">
                        <div style="font-weight:850; color:#0f172a;">{row['business_name']}</div>
                        <div style="color:#64748b; font-size:0.88rem; margin-top:4px;">{row['city']}, {row['state']}</div>
                        <div style="color:#334155; font-size:0.9rem; margin-top:8px;"><b>Stars:</b> {row['avg_stars']} &nbsp; <b>Reviews:</b> {int(row['total_reviews'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button("View Details", key=f"home_location_{row['business_name']}_{row['city']}_{row['state']}"):
                    st.session_state["selected_provider"] = row["business_name"]
                    st.switch_page("pages/1_Provider_Analysis.py")
else:
    st.info("No location data available for the selected filter.")

st.markdown("---")






st.markdown("## Explore care themes")
st.info("CarePulse converts patient review text into care-specific signals so users can understand what patients actually mention across provider experiences.")

theme_cards = [
    ("Doctor Care", "Clinical quality", "Diagnosis, treatment confidence, attention, and patient trust.", "app/assets/doctor_care.png"),
    ("Staff Behavior", "Service experience", "Front-desk support, friendliness, professionalism, and responsiveness.", "app/assets/staff_behavior.png"),
    ("Billing / Cost", "Cost transparency", "Insurance issues, charges, billing confusion, and payment concerns.", "app/assets/billing_cost.png"),
    ("Wait Time", "Access friction", "Appointment delays, long waits, scheduling pain points, and urgency.", "app/assets/wait_time.png"),
    ("Communication", "Patient clarity", "Clear explanations, follow-up instructions, and question handling.", "app/assets/communication.png"),
    ("Cleanliness", "Facility trust", "Clean rooms, comfort, physical environment, and overall care setting.", "app/assets/cleanliness.png"),
]

for i in range(0, len(theme_cards), 3):
    cols = st.columns(3)
    for col, (title, label, desc, img_path) in zip(cols, theme_cards[i:i+3]):
        with col:
            with st.container(border=True):
                if Path(img_path).exists():
                    st.image(img_path, use_container_width=True)
                st.subheader(title)
                st.caption(label)
                st.write(desc)

st.markdown("---")






f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Find trusted providers</div>
        <div class="feature-text">
            Explore high-quality providers using review volume, sentiment balance, and composite quality scoring instead of relying on stars alone.
        </div>
    </div>
    """, unsafe_allow_html=True)
with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Understand patient concerns</div>
        <div class="feature-text">
            Surface what patients mention most often, including billing, wait time, communication, staff behavior, and care quality.
        </div>
    </div>
    """, unsafe_allow_html=True)
with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Explore smarter care decisions</div>
        <div class="feature-text">
            Use aspect-aware review signals and location-aware provider exploration to identify stronger care options more confidently.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Featured providers")

provider_summary = (
    filtered_df.groupby(["business_name", "city", "state"])
    .agg(total_reviews=("review_id", "count"), avg_stars=("stars", "mean"))
    .reset_index()
)

cqi_df = (
    filtered_df.groupby("business_name")
    .apply(calculate_cqi)
    .reset_index(name="cqi_tuple")
)
cqi_df["cqi"] = cqi_df["cqi_tuple"].apply(lambda x: x[0])
cqi_df = cqi_df.drop(columns=["cqi_tuple"])

provider_summary = provider_summary.merge(cqi_df, on="business_name", how="left")
provider_summary["avg_stars"] = provider_summary["avg_stars"].round(2)
provider_summary["quality_band"] = provider_summary["cqi"].apply(quality_label)

featured = provider_summary.sort_values(["cqi", "total_reviews"], ascending=[False, False]).head(6)

card_rows = [featured.iloc[i:i+3] for i in range(0, min(len(featured), 6), 3)]

for row_df in card_rows:
    cols = st.columns(len(row_df))
    for col, (_, row) in zip(cols, row_df.iterrows()):
        with col:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.94); border:1px solid rgba(148,163,184,0.13); border-radius:22px; padding:20px; box-shadow:0 10px 24px rgba(15,23,42,0.05); min-height:220px;">
                    <div style="font-size:1.05rem; font-weight:800; color:#0f172a; margin-bottom:8px;">{row['business_name']}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-bottom:10px;">{row['city']}, {row['state']}</div>
                    <div style="margin-bottom:10px;">{quality_badge(row['cqi'])}</div>
                    <div style="font-size:0.95rem; color:#334155; margin-bottom:6px;"><b>CQI:</b> {row['cqi']}</div>
                    <div style="font-size:0.95rem; color:#334155; margin-bottom:6px;"><b>Stars:</b> {row['avg_stars']}</div>
                    <div style="font-size:0.95rem; color:#334155;"><b>Reviews:</b> {int(row['total_reviews'])}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("View Details", key=f"view_details_{row['business_name']}_{row['city']}_{row['state']}"):
                st.session_state["selected_provider"] = row["business_name"]
                st.switch_page("pages/1_Provider_Analysis.py")

st.markdown("---")

left, right = st.columns([1.1, 0.9])

with left:
    st.markdown("## Sentiment overview")
    sentiment_counts = filtered_df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]

    fig_sent = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        hole=0.58,
        title="Sentiment Mix"
    )
    fig_sent.update_layout(height=430)
    st.plotly_chart(fig_sent, use_container_width=True)

with right:
    st.markdown("## Most discussed themes")
    aspect_summary = []
    for col, label in ASPECT_LABELS.items():
        count = int(filtered_df[col].sum())
        pct = round((count / len(filtered_df)) * 100, 1) if len(filtered_df) else 0
        aspect_summary.append({"aspect": label, "count": count, "pct": pct})

    aspect_df = pd.DataFrame(aspect_summary).sort_values("count", ascending=False)

    fig_aspects = px.bar(
        aspect_df,
        x="count",
        y="aspect",
        orientation="h",
        text="pct",
        title="Top Mentioned Aspects"
    )
    fig_aspects.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_aspects.update_layout(height=430, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_aspects, use_container_width=True)

st.markdown("---")

st.markdown("## Regional review activity")

state_summary = (
    filtered_df.groupby("state")
    .size()
    .reset_index(name="reviews")
    .sort_values("reviews", ascending=False)
    .head(12)
)

fig_state = px.bar(
    state_summary,
    x="state",
    y="reviews",
    text="reviews",
    title="Top States by Review Volume"
)
fig_state.update_traces(textposition="outside")
fig_state.update_layout(height=420)
st.plotly_chart(fig_state, use_container_width=True)

st.markdown("---")

st.markdown("## Live sentiment analyzer")
st.caption("This analyzer now uses a DistilBERT transformer model.")

predict_col1, predict_col2 = st.columns([1.1, 1])

with predict_col1:
    review_text = st.text_area(
        "Review text",
        height=180,
        placeholder="Example: The doctor was very caring, but the front desk was rude and the billing process took too long."
    )

    if st.button("Analyze review"):
        if not review_text.strip():
            st.warning("Please enter a review first.")
        else:
            result = predict_distilbert_sentiment(review_text)
            st.session_state["cp_prediction"] = result["label"]
            st.session_state["cp_negative"] = result["negative"]
            st.session_state["cp_positive"] = result["positive"]
            st.session_state["cp_confidence"] = result["confidence"]

with predict_col2:
    if "cp_prediction" in st.session_state:
        metric_card(
            "Predicted Sentiment",
            st.session_state["cp_prediction"].upper(),
            f"Confidence: {st.session_state['cp_confidence']:.3f}"
        )

        prob_df = pd.DataFrame({
            "label": ["negative", "positive"],
            "score": [st.session_state["cp_negative"], st.session_state["cp_positive"]]
        })
        fig_prob = px.bar(prob_df, x="label", y="score", text="score", title="Confidence Scores")
        fig_prob.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_prob.update_layout(height=300, yaxis_range=[0, 1.05])
        st.plotly_chart(fig_prob, use_container_width=True)
    else:
        st.info("Run a review through the analyzer to see prediction output here.")

