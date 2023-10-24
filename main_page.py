import os
import streamlit as st
import pandas as pd
from streamlit import session_state
import datetime
import manage_patients
import category_page
import new_patient

def main(session_state):
    # Define the base directory where patient folders will be created
    base_dir = "patient_data"
    os.makedirs(base_dir, exist_ok=True)

    # Function to add a new patient --> def add_new_patient --> return patient_folder

    # Streamlit app
    st.title("Select Patient")

    # Get a list of existing patients
    existing_patients = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]

    # Create a dynamic dropdown for selecting an existing patient
    selected_patient = st.selectbox("Select a patient", existing_patients)
    if selected_patient:
        session_state.current_page = 'manage_patients'

    # Create a button to toggle between states
    if st.button("Add New Patient"): 
        session_state.current_page = 'new_patient'


