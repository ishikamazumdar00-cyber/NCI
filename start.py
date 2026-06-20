import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NCI Nagpur Review's Trend analysis",
    page_icon="🏥",
    layout="wide"
)

# ==========================
# LOAD GOOGLE SHEET
# ==========================

sheet_id = "1tF7Zb1oEg9LScv7PDK40kiud5vDJWyq-S6WcpG7C0rk"

reviews_df = pd.read_csv(
    f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
)

freq_df = reviews_df.copy()
dept_df = reviews_df.copy()

# ==========================
# HEADER
# ==========================

st.title("🏥 NCI Nagpur Training Needs Dashboard")
st.caption("Generated from Google Review Analysis")

# ==========================
# KPI CARDS
# ==========================

total_reviews = len(reviews_df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(reviews_df))
col2.metric("Average Rating", round(reviews_df["Star rating"].mean(), 2))
col3.metric("5-Star Reviews", len(reviews_df[reviews_df["Star rating"] == 5]))

# ==========================
# ISSUE FREQUENCY
# ==========================

st.divider()

st.subheader("Top Patient Complaints")

issue_data = freq_df.iloc[:, [0, 1]]

issue_data.columns = ["Issue", "Frequency"]

issue_data["Frequency"] = (
    issue_data["Frequency"]
    .astype(str)
    .str.extract(r'(\d+)')
    .astype(float)
)

reviews_df["Review date"] = pd.to_datetime(
    reviews_df["Review date"]
)

monthly_reviews = (
    reviews_df
    .groupby(reviews_df["Review date"].dt.to_period("M"))
    .size()
    .reset_index(name="Reviews")
)

monthly_reviews["Review date"] = monthly_reviews[
    "Review date"
].astype(str)

fig1 = px.line(
    monthly_reviews,
    x="Review date",
    y="Reviews",
    markers=True,
    title="Review Volume Trend Over Time"
)

st.plotly_chart(fig1, use_container_width=True)


# ==========================
# DEPARTMENT PRIORITY
# ==========================


# ==========================
# STAR RATING DISTRIBUTION
# ==========================

st.divider()

st.subheader("Star Rating Distribution")

rating_counts = (
    reviews_df["Star rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_counts.columns = [
    "Rating",
    "Count"
]

fig2 = px.bar(
    rating_counts,
    x="Rating",
    y="Count",
    title="Distribution of Star Ratings"
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================
# REVIEW CATEGORY BREAKDOWN
# ==========================

st.divider()

st.subheader("Rating Distribution")

rating_counts = (
    reviews_df["Star rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_counts.columns = [
    "Rating",
    "Count"
]

fig3 = px.pie(
    rating_counts,
    names="Rating",
    values="Count",
    title="Rating Distribution"
)

st.plotly_chart(fig3, use_container_width=True)



# ==========================
# RAW DATA
# ==========================

st.divider()

st.subheader("Categorized Reviews")

st.dataframe(
    reviews_df,
    use_container_width=True
)
