import streamlit as st
import time
import numpy as np
import pandas as pd
import database.db_utils as db
from dict_to_pdf.dict_to_pdf import dict_to_pdf
from streamlit_extras.app_logo import add_logo


st.set_page_config(page_title="Supervisor View", page_icon="📈")
add_logo("static/imgs/logo2.jpg", height=300)

st.markdown("# Supervisor View")
st.sidebar.header("Supervisor View")

# db.test_functions()

# Define your data
user_data = {
    'Turbine Repair': {'worker': 'Bob Baumeister', 'worker-id': '0152332', 'date':"29.04.2023"},
    'Turbine Inspection': {'worker': 'Dora Entdecker', 'worker-id': '0314533', 'date':"24.04.2023"},
    # Add as many users as you need...
}

# Display the data
unique_user = []
for name in db.get_all_users():
    # Display information

    if name.name not in unique_user:
        st.markdown(f'**Worker:  {name.name}**')
        unique_user.append(name.name)
    
    for report in db.get_reports(name.id):
        st.write(f'Task: {report.report_name} || Id: {name.id} || Date: {report.date}')

        # Add a button for additional info
        data_dict = {'name': name.name, 'title': report.report_name, 'task_desc': report.report_name, 'task_summary': report.summary, 'faith_score': report.score}
        # print(data_dict)

        pdf = dict_to_pdf(data_dict)
        with open("../pdfs/output.pdf", 'rb') as file:
            contents = file.read()
        st.download_button(label="Download Document", data = contents, file_name=report.report_name)# TODO need to add a method call to generate or display the pdf