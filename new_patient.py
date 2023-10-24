import os
import streamlit as st
import pandas as pd
from streamlit import session_state
import datetime
import manage_patients
import category_page

# Define the base directory where patient folders will be created
base_dir = "patient_data"
os.makedirs(base_dir, exist_ok=True)

def add_new_patient(name, owner, phone, email, breed, birth_year):
    # Create a folder for the patient using the phone number and name
    patient_folder = os.path.join(base_dir, f"{phone}_{name}")
    os.makedirs(patient_folder, exist_ok=True)
    
    # Create subdirectories for bloodworks and reports
    category_dir = os.path.join(patient_folder, "Leishmaniasis")
    os.makedirs(category_dir, exist_ok=True)
    
    reports_dir = os.path.join(patient_folder, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create a CSV file with general patient info
    patient_info = pd.DataFrame({
        "Name": [name],
        "Owner": [owner],
        "Phone": [phone],
        "Email": [email],
        "Breed": [breed],
        "Birth Year": [birth_year]
    })
    
    info_csv_path = os.path.join(patient_folder, "patient_info.csv")
    patient_info.to_csv(info_csv_path, index=False)
    
    return patient_folder

def main(session_state):
    new_patient_name = st.text_input("Name")
    new_patient_owner = st.text_input("Owner")
    new_patient_phone = st.text_input("Phone")
    new_patient_email = st.text_input("Email")
    new_patient_breed = st.text_input("Breed")
    new_patient_birth_year = st.number_input("Year of Birth", min_value=1900, max_value=2100, step=1)

    if st.button("Submit Patient") :
        if new_patient_name and new_patient_owner and new_patient_phone:
            patient_folder = add_new_patient(new_patient_name, new_patient_owner, new_patient_phone, new_patient_email, new_patient_breed, new_patient_birth_year)
            st.success(f"New patient '{new_patient_name}' created in folder: {patient_folder}")
        session_state.current_page = 'manage_patients'
    