import streamlit as st
import os
import streamlit as st
import pandas as pd
from streamlit import session_state
import datetime

# Define the base directory where patient folders will be created
base_dir = "patient_data"
os.makedirs(base_dir, exist_ok=True)


def add_new_category(patient_folder, category_name, category_date):
    # Create a subdirectory in the patient folder for the new category using the date and the category name
    category_folder = os.path.join(patient_folder, category_name + "_" + category_date)
    os.makedirs(category_folder, exist_ok=True)
    
    # Create subdirectories inside the category folder for reports and treatment
    reports_dir = os.path.join(category_folder, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    treatment_dir = os.path.join(category_folder, "treatment")
    os.makedirs(treatment_dir, exist_ok=True)
    
    return category_folder

def main():
    st.title("Add new Category")
    st.subheader("Add New Category")
    category_name = st.text_input("Category")
    category_date = datetime.datetime.now().strftime("%Y-%m-%d")

    existing_patients = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    selected_patient = st.sidebar.selectbox("Select a patient", existing_patients)
    selected_patient_folder = [folder for folder in os.listdir(base_dir) if selected_patient in folder][0]
    selected_patient_path = os.path.join(base_dir, selected_patient_folder)
    if st.button("Save Category") :
        if category_name:
            category_folder = add_new_category(selected_patient_path, category_name,category_date)
            st.success(f"New category '{category_name}' created in folder: {selected_patient_folder}")
            session_state.current_page = 'manage_patients'
