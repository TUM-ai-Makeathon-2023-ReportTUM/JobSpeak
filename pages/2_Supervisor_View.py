import streamlit as st
import time
import numpy as np
import pandas as pd

st.set_page_config(page_title="Supervisor View", page_icon="📈")

st.markdown("# Supervisor View")
st.sidebar.header("Supervisor View")

# Define your data
user_data = {
    'Turbine Repair': {'worker': 'Bob Baumeister', 'worker-id': '0152332', 'date':"29.04.2023"},
    'Turbine Inspection': {'worker': 'Dora Entdecker', 'worker-id': '0314533', 'date':"24.04.2023"},
    # Add as many users as you need...
}

# Display the data
for name, info in user_data.items():
    # Display information
    st.write(f'Task: {name} || Responsible: {info["worker"]} || Id: {info["worker-id"]} || Date: {info["date"]}')

    # Add a button for additional info
    if st.button(f'Create report for {name}'):
        print("Call some function...") # TODO need to add a method call to generate or display the pdf