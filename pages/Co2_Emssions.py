import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import numpy as np
import base64
import os

st.set_page_config(
    page_title="Emission Tracker",
    page_icon="🌎",  # Globe emoji as tab icon
    layout="wide"
)

globe_logo_path = "data/logoGLOBE.png"
if os.path.exists(globe_logo_path):
    st.markdown(
        f"""
        <div style="position: absolute; top: 30px; right: 30px;">
            <img src="data:image/png;base64,{base64.b64encode(open(globe_logo_path, "rb").read()).decode()}" alt="globe" width="80">
        </div>
        """,
        unsafe_allow_html=True
    )


# Get the absolute path to the data file
co2_data_path = os.path.join(os.path.dirname(__file__), "../data/Data_by_Vehicle.csv")

# Check if file exists before reading
if not os.path.exists(co2_data_path):
    st.error("Error: CO2 emissions data file was not found. Please check the file path.")
    st.stop()

# Load CO2 emissions data
df_co2 = pd.read_csv(co2_data_path)
df_co2.rename(columns={"Model Year": "Year", "Real-World CO2 (g/mi)": "CO2 Emissions", "Real-World CO2_City (g/mi)": "CO2 Emissions City", "Real-World CO2_Hwy (g/mi)": "CO2 Emissions Hwy"}, inplace=True)
df_co2["Year"] = pd.to_numeric(df_co2["Year"], errors='coerce').astype('Int64')
df_co2 = df_co2.dropna(subset=["Year", "CO2 Emissions"])

# Streamlit app title
st.title("CO2 Emissions by Vehicle Type Over Time")

# Allow user to select a date range
min_year = int(df_co2["Year"].min())
max_year = int(df_co2["Year"].max())
start_year, end_year = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Filter CO2 emissions data based on selected year range
filtered_co2_df = df_co2[(df_co2["Year"] >= start_year) & (df_co2["Year"] <= end_year)]

# Checkboxes for selecting vehicle types
st.sidebar.header("Select Vehicle Types:")
all_vehicle_types = df_co2["Vehicle Type"].unique()
selected_vehicle_types = []
for vehicle in all_vehicle_types:
    if st.sidebar.checkbox(vehicle, value=True, key=f"vehicle_{vehicle}"):
        selected_vehicle_types.append(vehicle)

# Filter CO2 emissions data based on selection
filtered_co2_df = filtered_co2_df[filtered_co2_df["Vehicle Type"].isin(selected_vehicle_types)]

# Create line chart for CO2 emissions
fig_co2 = px.line(
    filtered_co2_df, x="Year", y="CO2 Emissions", color="Vehicle Type",
    title="CO2 Emissions by Vehicle Type Over Time",
    labels={"CO2 Emissions": "CO2 Emissions (g/mi)"},
    color_discrete_sequence=px.colors.qualitative.Set1
)

# Enhance visualization
fig_co2.update_traces(line=dict(width=2))  # Thicker lines for better visibility
fig_co2.update_layout(
    height=500, margin=dict(l=40, r=40, t=40, b=40),
    hovermode="x unified",
    legend_title_text="Vehicle Type",
    title=dict(font=dict(size=18, family="Arial", color="white")),
    font=dict(family="Arial", size=14, color="white")
)
fig_co2.update_xaxes(showgrid=True, dtick=10, type="linear")  # Ensure Year is treated as a number
fig_co2.update_yaxes(showgrid=True, title_text="CO2 Emissions (g/mi)")

# Display chart
st.plotly_chart(fig_co2)

# Integration of Regulatory Class comparison chart
st.subheader("Compare Vehicle Types Based on Various Metrics")
df_co2["Footprint (sq. ft.)"] = df_co2["Footprint (sq. ft.)"].replace("-", np.nan)
df_co2["Footprint (sq. ft.)"] = pd.to_numeric(df_co2["Footprint (sq. ft.)"], errors="coerce")

st.write("Select the vehicle types you want to compare")
df_unique = df_co2["Regulatory Class"].unique()
selected_classes = []
for vehicle_class in df_unique:
    if st.checkbox(vehicle_class, value=True, key=f"class_{vehicle_class}"):
        selected_classes.append(vehicle_class)

filtered_df = df_co2[df_co2["Regulatory Class"].isin(selected_classes)]
filtered_df["Year"] = pd.to_numeric(filtered_df["Year"], errors='coerce').astype('Int64')  # Ensure Year is an integer
filtered_df = filtered_df.groupby(["Year", "Regulatory Class"], as_index=False).agg({
    "Real-World MPG": "mean",
    "Weight (lbs)": "mean",
    "Horsepower (HP)": "mean",
    "Real-World MPG_City": "mean",
    "Real-World MPG_Hwy": "mean",
    "CO2 Emissions": "mean",
    "CO2 Emissions City": "mean",
    "CO2 Emissions Hwy": "mean",
})

# Dropdown for metric selection
y_axis = st.selectbox("Select a metric to display:", [
    "Real-World MPG", "CO2 Emissions", "Weight (lbs)", "Horsepower (HP)",
    "Real-World MPG_City", "Real-World MPG_Hwy", "CO2 Emissions", "CO2 Emissions City", "CO2 Emissions Hwy"
])

if len(selected_classes) > 0:
    # Checkboxes for vertical lines
    show_1994 = st.checkbox("Show 1994: Tier 1 Emissions Standards", value=True)
    show_2004 = st.checkbox("Show 2004: Tier 2 Emissions Standards", value=True)
    show_2012 = st.checkbox("Show 2012: GHG Emissions Regulation", value=True)
    show_2017 = st.checkbox("Show 2017: Tier 3 Emissions Regulation", value=True)

    # Collect active regulation years and labels
    regulation_lines = []
    if show_1994:
        regulation_lines.append({'Year': 1994, 'Label': 'Tier 1'})
    if show_2004:
        regulation_lines.append({'Year': 2000, 'Label': 'Tier 2'})
    if show_2012:
        regulation_lines.append({'Year': 2012, 'Label': 'GHG'})
    if show_2017:
        regulation_lines.append({'Year': 2017, 'Label': 'Tier 3'})

    # Base line chart
    fuel_economy = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X("Year:O", title="Year", axis=alt.Axis(format="d")),
        y=alt.Y(y_axis, title=y_axis),
        color="Regulatory Class:N"
    )

    chart = fuel_economy

    if regulation_lines:
        regulation_df = pd.DataFrame(regulation_lines)

        vlines = alt.Chart(regulation_df).mark_rule(color='black').encode(
            x=alt.X('Year:O')
        )

        labels = alt.Chart(regulation_df).mark_text(
            align='left',
            baseline='bottom',
            dx=3,
            dy=-3
        ).encode(
            x=alt.X('Year:O'),
            text='Label'
        )

        chart += vlines + labels

    st.altair_chart(chart, use_container_width=True)

else:
    st.write("No vehicle type selected")


# Add link to Home.py in sidebar
st.sidebar.page_link("Home.py", label="Home")