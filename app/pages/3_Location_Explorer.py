import streamlit as st
import pandas as pd
import plotly.express as px

from app.utils import load_data

st.set_page_config(page_title="Location Explorer", layout="wide")

st.title("Explore Providers by Location")

reviews_df, businesses_df = load_data()

# --- Merge data ---
df = reviews_df.merge(
    businesses_df[["business_id", "name", "city", "state", "latitude", "longitude"]],
    on="business_id",
    how="left"
)

df = df.rename(columns={"name": "business_name"})

# --- Filters ---
states = ["All"] + sorted(df["state"].dropna().unique().tolist())
selected_state = st.selectbox("Select State", states)

if selected_state != "All":
    df = df[df["state"] == selected_state]

# --- Aggregate providers ---
provider_df = (
    df.groupby(["business_name", "city", "state", "latitude", "longitude"])
    .agg(
        avg_stars=("stars", "mean"),
        total_reviews=("stars", "count")
    )
    .reset_index()
)

provider_df = provider_df[provider_df["latitude"].notna()]

# --- Map ---
st.subheader("Provider Map")

fig = px.scatter_mapbox(
    provider_df,
    lat="latitude",
    lon="longitude",
    hover_name="business_name",
    hover_data=["city", "state", "avg_stars", "total_reviews"],
    size="total_reviews",
    zoom=4,
    height=600
)

fig.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig, use_container_width=True)

# --- Table ---
st.subheader("Providers List")

st.dataframe(
    provider_df.sort_values(by="total_reviews", ascending=False).head(50),
    use_container_width=True
)
