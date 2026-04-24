import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Electricity Access Dashboard",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_electricity_access.csv")

df = load_data()

# Title
st.title("🌍 Electricity Access Dashboard")

# Sidebar filter (basic)
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

# Filter data
filtered_df = df[df["year"] == year]

# Basic KPI
st.subheader("Key Metric")

avg_access = filtered_df["electricityAccess"].mean()
st.metric("Average Electricity Access (%)", f"{avg_access:.2f}")

# Simple table view
st.subheader("Data Preview")
st.dataframe(filtered_df.head(20))