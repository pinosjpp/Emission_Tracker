import streamlit as st
from PIL import Image
import os
import base64

# Set page config
st.set_page_config(
    page_title="Emission Tracker",
    page_icon="🌎",  # Globe emoji as tab icon
    layout="wide"
)

# Load Emission Tracker logo
logo_path = "data/logoE.png"
if os.path.exists(logo_path):
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" alt="logo" width="400">
        </div>
        """,
        unsafe_allow_html=True
    )
    

# Title and Text
st.title("Welcome to the Emission Tracker Dashboard")

st.write("""
This dashboard provides interactive insights into:
- Motor vehicle registrations across U.S. states over time.
- Real-world CO2 emissions trends based on vehicle types.
- Fuel efficiency and environmental impact of different vehicles.

Use the sidebar to navigate across different analysis pages!
""")

st.header("Navigation")
st.markdown("""
- **Registrations**: Explore vehicle registrations and trends by state.
- **CO2 Emissions**: Analyze CO2 emissions and compare vehicle types.
- **Manufacturer Analysis**: Dive deeper into manufacturer-specific vehicle data.
""")

# Divider
st.markdown("---")

# Footer
st.write("""
Built with 🚀 using Streamlit.

Maintained by [@TEAM13](https://github.com/pinosjpp/Emission_Tracker)
""")