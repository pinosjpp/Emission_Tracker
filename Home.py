import streamlit as st

st.set_page_config(page_title="Motor Vehicle Dashboard", layout="wide")

# Homepage title
st.title("Welcome to the Motor Vehicle Dashboard")

#change as project developes 
st.markdown(
    """
    This dashboard provides insights into motor vehicle registrations across different states and time periods.
    Use the navigation sidebar to explore the data by selecting a state and filtering by year range.
    
    ### Features:
    - Co2 Emmisons
    - Interactive charts for vehicle registrations.
    - Select and filter data by state and year range.
    - Compare different vehicle types over time.
    """
)


st.sidebar.header("Navigation")
st.sidebar.write("Use the sidebar to access different sections of the dashboard.")