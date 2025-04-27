import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import numpy as np
import os

st.set_page_config(
    page_title="Emission Tracker",
    page_icon="🌎",  # Globe emoji as tab icon
    layout="wide"
)


# Get the absolute path to the data file
co2_data_path = os.path.join(os.path.dirname(__file__), "../data/Manufacturer_Response.csv")

# Check if file exists before reading
if not os.path.exists(co2_data_path):
    st.error("Error: CO2 emissions data file was not found. Please check the file path.")
    st.stop()


st.title("Manufacturer CO2 Emissions Data")

#converts data to ints and grups by manufactuer
dfmanufacturer = pd.read_csv(co2_data_path)
dfmanufacturer["Model Year"] = pd.to_numeric(dfmanufacturer["Model Year"], errors='coerce').astype('Int64')
dfmanufacturer["Real-World MPG"] =pd.to_numeric(dfmanufacturer["Real-World MPG"], errors='coerce').astype('Float64')
dfmanufacturer["Real-World MPG_City"] = pd.to_numeric(dfmanufacturer["Real-World MPG_City"], errors='coerce').astype('Float64')
dfmanufacturer["Real-World MPG_Hwy"] = pd.to_numeric(dfmanufacturer["Real-World MPG_Hwy"], errors='coerce').astype('Float64')
dfmanufacturer["Real-World CO2 (g/mi)"] = pd.to_numeric(dfmanufacturer["Real-World CO2 (g/mi)"], errors='coerce').astype('Float64')
dfmanufacturer["Real-World CO2_City (g/mi)"] =pd.to_numeric(dfmanufacturer["Real-World CO2_City (g/mi)"], errors='coerce').astype('Float64')
dfmanufacturer["Real-World CO2_Hwy (g/mi)"] = pd.to_numeric(dfmanufacturer["Real-World CO2_Hwy (g/mi)"], errors='coerce').astype('Float64')
dfmanufacturer["Weight (lbs)"] = pd.to_numeric(dfmanufacturer["Weight (lbs)"], errors='coerce').astype('Float64')
dfmanufacturer["Horsepower (HP)"] = pd.to_numeric(dfmanufacturer["Horsepower (HP)"], errors='coerce').astype('Float64')



dfmanufacturer = dfmanufacturer.groupby(["Manufacturer", "Model Year"]).mean(numeric_only=True).reset_index()
print(dfmanufacturer.head(200))

df_co2 = pd.read_csv(co2_data_path)
df_co2.rename(columns={"Model Year": "Year", "Real-World CO2 (g/mi)": "CO2 Emissions", "Real-World CO2_City (g/mi)": "CO2 Emissions City", "Real-World CO2_Hwy (g/mi)": "CO2 Emissions Hwy"}, inplace=True)
df_co2["Year"] = pd.to_numeric(df_co2["Year"], errors='coerce').astype('Int64')
df_co2 = df_co2.dropna(subset=["Year", "CO2 Emissions"])


st.subheader("Trends Over Time by Manufacturer")

# List of numeric columns to choose from
y_axis_options = {
    "Real-World MPG": "Real-World MPG",
    "Real-World MPG (City)": "Real-World MPG_City",
    "Real-World MPG (Highway)": "Real-World MPG_Hwy",
    "CO2 Emissions": "Real-World CO2 (g/mi)",
    "CO2 Emissions (City)": "Real-World CO2_City (g/mi)",
    "CO2 Emissions (Highway)": "Real-World CO2_Hwy (g/mi)",
    "Weight (lbs)": "Weight (lbs)",
    "Horsepower (HP)": "Horsepower (HP)"
}

# Dropdown to select Y-axis metric
selected_y_label = st.selectbox("Select metric to plot:", list(y_axis_options.keys()))
selected_y_col = y_axis_options[selected_y_label]

# Manufacturer selection
manufacturers = dfmanufacturer["Manufacturer"].dropna().unique()
selected_manufacturers = st.multiselect("Select Manufacturer(s):", sorted(manufacturers), default=manufacturers[:3])

# Regulation year filter (with "All Years" option)
start_year_option = st.selectbox(
    "Start data from regulation year:",
    ["All Years", 1994, 2000, 2012, 2017],
    index=0
)

# Filter data
if start_year_option == "All Years":
    filtered_df = dfmanufacturer[dfmanufacturer["Manufacturer"].isin(selected_manufacturers)]
else:
    filtered_df = dfmanufacturer[
        (dfmanufacturer["Manufacturer"].isin(selected_manufacturers)) &
        (dfmanufacturer["Model Year"] >= int(start_year_option))
    ]



# Create line chart
fig = px.line(
    filtered_df,
    x="Model Year",
    y=selected_y_col,
    color="Manufacturer",
    title=f"{selected_y_label} Over Time",
    labels={selected_y_col: selected_y_label, "Model Year": "Model Year"}
)

fig.update_layout(height=500, margin=dict(l=40, r=40, t=40, b=40))
st.plotly_chart(fig)
