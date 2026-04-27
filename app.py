import streamlit as st
import pandas as pd
import plotly.express as px

COLOR_PRIMARY = "#2E86AB"
COLOR_SECONDARY = "#F18F01"
COLOR_ALERT = "#C0392B"
COLOR_GOOD      = "#50c878"

st.set_page_config(page_title="Global Electricity Access Dashboard",page_icon="⚡",
                   layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_electricity_access.csv")
    df["year"] = df["year"].astype(int)
    df["electricityAccess"] = df["electricityAccess"].astype(float)
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
col1, col2, col3, col4 = st.columns(4)

global_avg = filtered_df["electricityAccess"].mean()
countries_100 = filtered_df[filtered_df["electricityAccess"] >= 99].shape[0]
countries_low = filtered_df[filtered_df["electricityAccess"] < 60].shape[0]
worst_row = filtered_df.nsmallest(1, "electricityAccess")

col1.metric("🌍 Global Avg Access", f"{global_avg:.1f}%")
col2.metric("⚡ Countries with 100% Access", countries_100)
col3.metric("⚠ Countries Below 60%", countries_low)
col4.metric("🔻 Worst Performing Country",
    worst_row["countryName"].values[0],
    f"{worst_row['electricityAccess'].values[0]:.1f}%")

st.divider()

# Global trend over time
st.subheader("📈 Global Electricity Access Trend")

trend = df.groupby("year")["electricityAccess"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="year",
    y="electricityAccess",
    markers=True,
    title="Average Global Electricity Access Over Time",
    labels={"electricityAccess": "Access (%)", "year": "Year"}
)

st.plotly_chart(fig_trend, use_container_width=True)
fig_trend = px.line(
    trend,
    x="year",
    y="electricityAccess",
    markers=True,
    title="Average Global Electricity Access Over Time",
    labels={"electricityAccess": "Electricity Access (%)", "year": "Year"}
)

fig_trend.update_traces(line=dict(color=COLOR_PRIMARY, width=3))
fig_trend.update_layout(
    title_x=0.3,
    yaxis_title="Electricity Access (%)",
    xaxis_title="Year")

# Region comparison
st.subheader("🌎 Electricity Access by Region")

interesting_regions = [
    "South Asia", "Sub-Saharan Africa",
    "Middle East & North Africa",
    "Latin America & Caribbean",
    "East Asia & Pacific"
]

region_avg = df[df["region"].isin(interesting_regions)].groupby(
    ["year", "region"])["electricityAccess"].mean().reset_index()

fig_region = px.line(
    region_avg,
    x="year",
    y="electricityAccess",
    color="region",
    markers=True,
    title="Regional Electricity Access Trends (Developing Regions)",
    labels={"electricityAccess": "Access (%)", "year": "Year"},
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig_region.update_layout(
    title_x=0.3,
    legend_title="Region",
    yaxis=dict(range=[0, 105])
)
st.plotly_chart(fig_region, use_container_width=True)

st.divider()

# Top countries and Bottom countries
st.subheader("🏆 Top Countries with Highest Access")
st.subheader(f"📊 Country Rankings ({selected_year})")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**🏆 Top 10 - Developing Regions**")
    developing_regions = ["South Asia", "Sub-Saharan Africa", "Middle East & North Africa"]
    top_countries = filtered_df[filtered_df["region"].isin(developing_regions)] \
        .sort_values("electricityAccess", ascending=False).head(10)

    fig_top = px.bar(
        top_countries,
        x="electricityAccess",
        y="countryName",
        orientation="h",
        color="electricityAccess",
        color_continuous_scale=["#e05c5c", "#f0c040", COLOR_GOOD],
        range_color=[0, 100],
        labels={"electricityAccess": "Access (%)", "countryName": ""}
    )
    fig_top.update_layout(
        xaxis=dict(range=[0, 105]),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_top, use_container_width=True)

with col_right:
    st.markdown("**⚠️ Bottom 10 - Lowest Access**")
    bottom_countries = filtered_df.sort_values("electricityAccess").head(10)

    fig_bottom = px.bar(
        bottom_countries,
        x="electricityAccess",
        y="countryName",
        orientation="h",
        color="electricityAccess",
        color_continuous_scale=["#C0392B", "#F18F01", COLOR_GOOD],
        range_color=[0, 60],
        labels={"electricityAccess": "Access (%)", "countryName": ""}
    )
    fig_bottom.update_layout(
        xaxis=dict(range=[0, 105]),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_bottom, use_container_width=True)

st.divider()

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

# Country Trend Analysis 
st.subheader("📊 Country Trend Analysis")

country = st.selectbox("Select Country", sorted(df["countryName"].unique()))

country_df = df[df["countryName"] == country]
last_10_years = sorted(country_df["year"].unique())[-10:]
country_df_filtered = country_df[country_df["year"].isin(last_10_years)]

fig_country = px.bar(
    country_df_filtered,
    x="year",
    y="electricityAccess",
    text="electricityAccess",
    title=f"Electricity Access (Last 10 Years) — {country}",
    labels={"electricityAccess": "Access (%)", "year": "Year"},
    color="electricityAccess",
    color_continuous_scale=["#e05c5c", "#f0c040", COLOR_GOOD],
    range_color=[0, 100]
)
fig_country.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_country.update_layout(
    title_x=0.3,
    xaxis=dict(tickmode='linear'),
    yaxis=dict(range=[0, 110]),
    coloraxis_showscale=False
)
st.plotly_chart(fig_country, use_container_width=True)

st.divider()

#Country Deep Dive
st.subheader("🔍 Country Deep Dive")

country = st.selectbox("Select a Country", sorted(df["countryName"].unique()))
country_df = df[df["countryName"] == country]

first_val = country_df.nsmallest(1, "year")["electricityAccess"].values[0]
last_val  = country_df.nlargest(1,  "year")["electricityAccess"].values[0]
change    = last_val - first_val

c1, c2, c3 = st.columns(3)
c1.metric("📅 Access in 2000", f"{first_val:.1f}%")
c2.metric("📅 Access in 2023", f"{last_val:.1f}%")
c3.metric("📈 Total Change",   f"{change:+.1f}%")

fig_country = px.area(
    country_df,
    x="year",
    y="electricityAccess",
    markers=True,
    title=f"Electricity Access Trend — {country}",
    labels={"electricityAccess": "Access (%)", "year": "Year"}
)
fig_country.update_traces(
    line=dict(color=COLOR_SECONDARY, width=3),
    fillcolor="rgba(46,134,171,0.15)"
)
fig_country.update_layout(
    title_x=0.3,
    yaxis=dict(range=[0, 105])
)
st.plotly_chart(fig_country, use_container_width=True)

st.divider()

# Dataset preview
st.subheader("📂 Dataset Preview")
st.dataframe(df.head(50))

#Footer - Dataset source
st.markdown("---")
st.caption("📊 Data: World Bank World Development Indicators | Indicator: WB_WDI_EG_ELC_ACCS_ZS | Years: 2000–2023")


