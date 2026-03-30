import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

DATA_PATH = Path("data/processed/healthcare_reviews_min20_labeled.csv")
ASPECT_PATH = Path("data/processed/healthcare_reviews_min20_aspects.csv")
BIZ_PATH = Path("data/processed/healthcare_businesses_min20.csv")
MODEL_PATH = Path("models/logreg_model.pkl")
VECTORIZER_PATH = Path("models/tfidf_vectorizer.pkl")

@st.cache_data
def load_data():
    reviews = pd.read_csv(DATA_PATH)
    businesses = pd.read_csv(BIZ_PATH)
    return reviews, businesses

@st.cache_data
def load_aspect_data():
    return pd.read_csv(ASPECT_PATH)

@st.cache_resource
def load_model_artifacts():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def inject_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7fcfb 0%, #eff8f6 45%, #f9fcfb 100%);
    }

    .main > div {
        padding-top: 0.8rem;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .cp-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(148,163,184,0.14);
        backdrop-filter: blur(10px);
        padding: 14px 18px;
        border-radius: 22px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }

    .cp-logo-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .cp-logo-icon {
        width: 42px;
        height: 42px;
        border-radius: 14px;
        background: linear-gradient(135deg, #0f766e, #14b8a6);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
        font-weight: 800;
        box-shadow: 0 6px 18px rgba(20,184,166,0.28);
    }

    .cp-logo-text {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.03em;
    }

    .cp-logo-sub {
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 2px;
    }

    .hero {
        background: linear-gradient(135deg, #0f766e, #115e59 45%, #0ea5a4 100%);
        padding: 34px 36px;
        border-radius: 28px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 14px 34px rgba(15, 118, 110, 0.16);
    }

    .hero h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 850;
        letter-spacing: -0.04em;
    }

    .hero p {
        margin-top: 14px;
        margin-bottom: 0;
        font-size: 1.03rem;
        color: #ecfeff;
        max-width: 980px;
        line-height: 1.6;
    }

    .metric-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(6px);
        padding: 18px 20px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
        border: 1px solid rgba(148, 163, 184, 0.13);
    }

    .metric-label {
        font-size: 0.92rem;
        color: #64748b;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 850;
        color: #0f172a;
        line-height: 1.1;
    }

    .metric-sub {
        margin-top: 6px;
        font-size: 0.85rem;
        color: #94a3b8;
    }

    .soft-card {
        background: rgba(255,255,255,0.9);
        padding: 18px;
        border-radius: 20px;
        border: 1px solid rgba(148,163,184,0.13);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .badge-green { background: rgba(34,197,94,0.14); color: #15803d; }
    .badge-yellow { background: rgba(250,204,21,0.18); color: #a16207; }
    .badge-orange { background: rgba(249,115,22,0.16); color: #c2410c; }
    .badge-red { background: rgba(239,68,68,0.16); color: #b91c1c; }

    .chip {
        display: inline-block;
        background: #dff7f4;
        color: #115e59;
        padding: 7px 11px;
        margin: 4px 6px 4px 0;
        border-radius: 999px;
        font-size: 0.84rem;
        font-weight: 700;
    }

    .feature-card {
        background: rgba(255,255,255,0.95);
        border-radius: 22px;
        padding: 22px;
        border: 1px solid rgba(148,163,184,0.12);
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
        min-height: 210px;
    }

    .feature-title {
        font-size: 1.28rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .feature-text {
        color: #475569;
        line-height: 1.6;
        font-size: 0.98rem;
    }

    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #0f766e, #14b8a6);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        box-shadow: 0 8px 18px rgba(20,184,166,0.18);
    }

    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #115e59, #0f766e);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def render_top_nav(current="Home"):
    st.markdown("""
    <div class="cp-nav">
        <div class="cp-logo-wrap">
            <div class="cp-logo-icon">✚</div>
            <div>
                <div class="cp-logo-text">CarePulse</div>
                <div class="cp-logo-sub">Healthcare review intelligence</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.page_link("Home.py", label="Home", icon="🏠")
    with c2:
        st.page_link("pages/1_Provider_Analysis.py", label="Provider Details", icon="🏥")
    with c3:
        st.page_link("pages/2_Find_the_One_for_You.py", label="Find the One for You", icon="🧭")

def metric_card(label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def calculate_cqi(provider_df):
    total_reviews = len(provider_df)
    avg_stars = provider_df["stars"].mean()

    sentiment_counts = provider_df["sentiment"].value_counts()
    positive = sentiment_counts.get("positive", 0)
    negative = sentiment_counts.get("negative", 0)

    star_score = (avg_stars / 5.0) * 100
    sentiment_balance = (positive - negative) / total_reviews if total_reviews > 0 else 0
    sentiment_score = ((sentiment_balance + 1) / 2) * 100
    volume_score = min(total_reviews / 200, 1.0) * 100

    cqi = 0.4 * star_score + 0.4 * sentiment_score + 0.2 * volume_score
    return round(cqi, 2), round(star_score, 2), round(sentiment_score, 2), round(volume_score, 2)

def quality_label(cqi):
    if cqi >= 85:
        return "Excellent"
    elif cqi >= 70:
        return "Good"
    elif cqi >= 55:
        return "Moderate"
    return "Poor"

def quality_badge(cqi):
    label = quality_label(cqi)
    if label == "Excellent":
        cls = "badge badge-green"
    elif label == "Good":
        cls = "badge badge-yellow"
    elif label == "Moderate":
        cls = "badge badge-orange"
    else:
        cls = "badge badge-red"
    return f'<span class="{cls}">{label}</span>'
