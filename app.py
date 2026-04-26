import streamlit as st
import pandas as pd
import plotly.express as px
COLOR_PRIMARY = "#2E86AB"
COLOR_SECONDARY = "#F18F01"
COLOR_ALERT = "#C0392B"

# Page config
st.set_page_config(page_title="Global Electricity Access Dashboard",
                   layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_electricity_access.csv")
    return df

df = load_data()

# Title
st.title("🌍 Global Electricity Access Dashboard")
st.markdown("Analysis of electricity access across countries and regions (2000–2023)")

# Sidebar filters
st.sidebar.header("Filters")

years = sorted(df['year'].unique())
selected_year = st.sidebar.slider("Select Year", int(min(years)), int(max(years)), int(max(years)))

regions = st.sidebar.multiselect(
    "Select Region",
    df['region'].unique(),
    default=df['region'].unique()
)

filtered_df = df[(df["year"] == selected_year) & (df["region"].isin(regions))]

# KPIs
col1, col2, col3 = st.columns(3)

global_avg = filtered_df["electricityAccess"].mean()
countries_100 = filtered_df[filtered_df["electricityAccess"] >= 99].shape[0]
countries_low = filtered_df[filtered_df["electricityAccess"] < 60].shape[0]

col1.metric("🌍 Global Avg Access", f"{global_avg:.1f}%")
col2.metric("⚡ Countries with 100% Access", countries_100)
col3.metric("⚠ Countries Below 60%", countries_low)

st.divider()

# Global trend over time
fig_trend = px.line(
    trend,
    x="year",
    y="electricityAccess",
    markers=True,
    title="Average Global Electricity Access Over Time",
)

fig_trend.update_traces(line=dict(color=COLOR_PRIMARY, width=3))
fig_trend.update_layout(
    title_x=0.3,
    yaxis_title="Access (%)",
    xaxis_title="Year")

# Region comparison
st.subheader("🌎 Electricity Access by Region")

region_avg = df.groupby(["year", "region"])["electricityAccess"].mean().reset_index()

fig_region = px.line(
    region_avg,
    x="year",
    y="electricityAccess",
    color="region",
    title="Regional Electricity Access Trends"
)

st.plotly_chart(fig_region, use_container_width=True)

# Top countries
st.subheader("🏆 Top Countries with Highest Access")

top_countries = filtered_df.sort_values("electricityAccess", ascending=False).head(10)

fig_top = px.bar(
    top_countries,
    x="electricityAccess",
    y="countryName",
    orientation="h",
    title="Top 10 Countries (Electricity Access)"
)

st.plotly_chart(fig_top, use_container_width=True)

# Bottom countries
st.subheader("⚠ Countries with Lowest Access")

bottom_countries = filtered_df.sort_values("electricityAccess").head(10)

fig_bottom = px.bar(
    bottom_countries,
    x="electricityAccess",
    y="countryName",
    orientation="h",
    title="Bottom 10 Countries"
)

st.plotly_chart(fig_bottom, use_container_width=True)

# Map visualization
st.subheader("🗺 Global Electricity Access Map")

map_df = df[df["year"] == selected_year]

fig_map = px.choropleth(
    map_df,
    locations="countryCode",
    color="electricityAccess",
    hover_name="countryName",
    color_continuous_scale="YlGn",
    title=f"Electricity Access by Country ({selected_year})"
)

st.plotly_chart(fig_map, use_container_width=True)

# Country trend analysis
st.subheader("📊 Country Trend Analysis")

country = st.selectbox("Select Country", df["countryName"].unique())

country_df = df[df["countryName"] == country]

fig_country = px.line(
    country_df,
    x="year",
    y="electricityAccess",
    markers=True,
    title=f"Electricity Access Trend - {country}"
)

st.plotly_chart(fig_country, use_container_width=True)

# Dataset preview
st.subheader("📂 Dataset Preview")
st.dataframe(df.head(50))

