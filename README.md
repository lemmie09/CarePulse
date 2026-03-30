
# CarePulse — Healthcare Review Intelligence Platform

CarePulse is a healthcare analytics platform that converts patient reviews into structured insights for evaluating provider quality and supporting informed decision-making.

Instead of relying solely on star ratings, the system analyzes review text to extract sentiment and care-specific themes, and aggregates these signals into a unified provider-level view.

---

## Overview

The platform integrates data processing, machine learning, and interactive visualization to provide:

* Provider-level performance insights
* Sentiment-based analysis of patient reviews
* Aspect-level understanding of care quality
* A composite scoring mechanism for ranking providers
* A discovery interface for matching providers to user needs

---

## Key Features

### Provider Analysis

* Search and filter healthcare providers
* View aggregated metrics such as review count, average rating, and sentiment distribution
* Composite Quality Index (CQI) for overall evaluation

### Sentiment Classification

* Binary sentiment model (positive / negative)
* Built using TF-IDF vectorization and Logistic Regression
* Accuracy: approximately 96%

### Aspect Extraction

Reviews are analyzed for key care dimensions:

* Doctor care
* Staff behavior
* Wait time
* Billing and cost
* Communication
* Cleanliness and facility

### Interactive Dashboard

* Dataset-level sentiment distribution
* Most discussed care themes
* Provider-level breakdowns

### Care-Based Discovery

* Users can select a care need or concern
* The system recommends providers based on:

  * CQI score
  * Sentiment patterns
  * Relevant care aspects

### Geographic Visualization

* Provider locations displayed on an interactive map
* Color-coded based on quality score

---

## Dataset

* Source: Yelp Academic Dataset
* Filtered for healthcare-related businesses
* Providers: approximately 2,400
* Reviews: approximately 105,000

### Data Processing Pipeline

* Category-based filtering for healthcare providers
* Minimum review threshold (at least 20 reviews per provider)
* Review extraction using business identifiers
* Sentiment labeling:

  * 1–2 stars: negative
  * 3 stars: neutral
  * 4–5 stars: positive
* Text cleaning and normalization

---

## Model Details

* TF-IDF vectorization

  * max_features: 20,000
  * ngram_range: (1, 2)
  * stop words removed

* Logistic Regression

  * max_iter: 1000

* Neutral reviews excluded for binary classification

* Performance:

  * Accuracy: 96.26%

---

## Composite Quality Index (CQI)

The CQI aggregates multiple signals to evaluate providers:

* Average rating
* Sentiment distribution
* Aspect-level indicators

This score is used for:

* Ranking providers
* Powering recommendations
* Driving map-based visualization

---

## Technology Stack

### Backend

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn

### Frontend and Visualization

* Streamlit
* Plotly
* PyDeck

---

## Project Structure

```
CarePulse/
├── app/                # Streamlit application
├── src/                # Data processing and modeling scripts
├── models/             # Saved model artifacts
├── data/               # Processed datasets (not fully included)
├── requirements.txt
└── README.md
```

---

## Running the Application

```bash
pip install -r requirements.txt
streamlit run app/Home.py
```

---

## Future Work

* Incorporation of transformer-based NLP models
* Improved aspect extraction techniques
* Real-time data ingestion and updates
* Deployment as a full web application
* Personalization based on user preferences

