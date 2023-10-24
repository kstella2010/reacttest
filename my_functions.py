
import os
import streamlit as st
import pandas as pd
from streamlit import session_state

# Define the base directory where patient folders will be created
base_dir = "patient_data"
os.makedirs(base_dir, exist_ok=True)


with category_section:

            st.subheader("Upload Reports")
            report_file = st.file_uploader("Upload a PDF file", type=["pdf"])
            
            if report_file:
                # Save the uploaded bloodwork file to the patient's directory
                file_path = os.path.join(base_dir, selected_patient_folder, "Leishmaniasis", report_file.name)
                with open(file_path, "wb") as f:
                    f.write(report_file.read())
                st.success(f"File '{report_file.name}' uploaded successfully.")
            
            # List existing bloodwork files and display their content
            category_files = os.listdir(os.path.join(base_dir, selected_patient_folder, "Leishmaniasis"))
            if category_files:
                st.subheader("Existing Files")
                for file in category_files:
                    st.write(file)
            else:
                st.info("No files available.")
            


