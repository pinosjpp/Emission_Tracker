import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Emission Tracker",
    page_icon="🌎",  # Globe emoji as tab icon
    layout="wide"
)

# Get the absolute path to the data file
data_path = os.path.join(os.path.dirname(__file__), "../data/Motor_Vehicle_Registrations_Dashboard_data.csv")

# Check if file exists before reading
if not os.path.exists(data_path):
    st.error("Error: Vehicle registration data file was not found. Please check the file path.")
    st.stop()

# Load vehicle registration data
df = pd.read_csv(data_path)
df.rename(columns={"year": "Year"}, inplace=True)
df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)

# Mapping full state names to abbreviations
state_abbreviations = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

df["state"] = df["state"].map(state_abbreviations)

#title
st.title("Motor Vehicle Registrations Dashboard")

#Map for Vehicle Registrations by State
st.subheader("Vehicle Registrations by State")
selected_map_year = st.slider("Select Year for Map:", min_value=1900, max_value=2020, value=2020)
exclude_california = st.toggle("Exclude California", value=False)

# Checkboxes for vehicle types to include
st.sidebar.header("Select Vehicle Types to Include:")
include_auto = st.sidebar.checkbox("Auto", value=True)
include_bus = st.sidebar.checkbox("Bus", value=True)
include_truck = st.sidebar.checkbox("Truck", value=True)
include_motorcycle = st.sidebar.checkbox("Motorcycle", value=True)

map_df = df[df["Year"] == selected_map_year]
if exclude_california:
    map_df = map_df[map_df["state"] != "CA"]

#sum only the selected vehicle types
selected_columns = []
if include_auto:
    selected_columns.append("Auto")
if include_bus:
    selected_columns.append("Bus")
if include_truck:
    selected_columns.append("Truck")
if include_motorcycle:
    selected_columns.append("Motorcycle")

if selected_columns:
    map_df["Total Vehicles"] = map_df[selected_columns].sum(axis=1)
else:
    map_df["Total Vehicles"] = 0  #default to zero

map_df = map_df.dropna(subset=["state", "Total Vehicles"])

if not map_df.empty:
    fig_map = px.choropleth(
        map_df, locations="state", locationmode="USA-states", color="Total Vehicles",
        hover_name="state", title=f"Total Vehicle Registrations in {selected_map_year}",
        color_continuous_scale="blues", scope="usa"
    )
    fig_map.update_layout(height=500, margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig_map)
else:
    st.warning("No data available for the selected year.")

#Layout for controls
col1, col2 = st.columns([1, 3])

with col1:
    #selecting state
    states = df["state"].dropna().unique()
    selected_state = st.selectbox("Select a State:", states)

    # Allow user to select a date range
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())
    start_year, end_year = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))


    # Checkbox controls for vertical lines
    show_1975 = st.checkbox("Show 1975: CAFE Standards", value=True)
    show_1994 = st.checkbox("Show 1994: Tier 1 Emissions", value=True)
    show_2004 = st.checkbox("Show 2004: Tier 2 Emissions", value=True)
    show_2012 = st.checkbox("Show 2012: GHG Emissions", value=True)
    show_2017 = st.checkbox("Show 2017: Tier 3 Emissions", value=True)

# Filter registration data based on state and selected year range
filtered_df = df[(df["state"] == selected_state) & (df["Year"] >= start_year) & (df["Year"] <= end_year)]

# Melt dataframe for plotting different vehicle types
melted_df = filtered_df.melt(id_vars=["Year"], value_vars=["Auto", "Bus", "Truck", "Motorcycle"], var_name="Vehicle Type", value_name="Registrations")


with col2:
    fig_reg = px.line(melted_df, x="Year", y="Registrations", color="Vehicle Type", title=f"Vehicle Registrations in {selected_state}", labels={"Registrations": "Number of Registrations"})
    # Add lines based on checkboxes
    if show_1975:
        fig_reg.add_vline(x=1975, line_dash="dash", line_color="black", annotation_text="CAFE Standards", annotation_position="top right")
    if show_1994:
        fig_reg.add_vline(x=1994, line_dash="dash", line_color="black", annotation_text="Tier 1", annotation_position="top right")
    if show_2004:
        fig_reg.add_vline(x=2004, line_dash="dash", line_color="black", annotation_text="Tier 2", annotation_position="top right")
    if show_2012:
        fig_reg.add_vline(x=2012, line_dash="dash", line_color="black", annotation_text="GHG", annotation_position="top right")
    if show_2017:
        fig_reg.add_vline(x=2017, line_dash="dash", line_color="black", annotation_text="Tier 3", annotation_position="top right")
    fig_reg.update_layout(height=500, margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig_reg)

# Add link to Home.py and CO2 page in sidebar
st.sidebar.page_link("Home.py", label="Home")