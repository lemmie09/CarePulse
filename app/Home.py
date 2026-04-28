import streamlit as st
import pandas as pd
import plotly.express as px
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

top1, top2 = st.columns([2.2, 1])

provider_names = sorted(reviews_df["business_name"].dropna().unique().tolist())
state_options = ["All"] + sorted(reviews_df["state"].dropna().unique().tolist())

with top1:
    selected_provider = st.selectbox("Search provider", ["None"] + provider_names, index=0)
with top2:
    selected_state = st.selectbox("Filter by state", state_options, index=0)

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

st.markdown("## Explore care themes")
aspect_cols = st.columns(6)
for col, label in zip(aspect_cols, ASPECT_LABELS.values()):
    with col:
        st.markdown(f'<span class="chip">{label}</span>', unsafe_allow_html=True)

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

st.markdown("---")

if selected_provider != "None":
    st.markdown("## Selected provider quick summary")

    selected_df = filtered_df[filtered_df["business_name"] == selected_provider].copy()

    if not selected_df.empty:
        cqi, _, _, _ = calculate_cqi(selected_df)
        selected_city = selected_df["city"].mode()[0] if not selected_df["city"].mode().empty else "N/A"
        selected_state_real = selected_df["state"].mode()[0] if not selected_df["state"].mode().empty else "N/A"
        selected_avg_star = round(selected_df["stars"].mean(), 2)
        selected_count = len(selected_df)

        q1, q2, q3, q4 = st.columns(4)
        with q1:
            metric_card("Provider", selected_provider, f"{selected_city}, {selected_state_real}")
        with q2:
            metric_card("CQI", cqi, f"Band: {quality_label(cqi)}")
        with q3:
            metric_card("Avg Stars", selected_avg_star, "Provider rating average")
        with q4:
            metric_card("Reviews", f"{selected_count:,}", "Provider review volume")

        st.caption("Use Provider Details from the top navigation to view full provider review analysis.")
