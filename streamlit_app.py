import os
import streamlit as st
import pandas as pd
from streamlit import session_state

# Define the base directory where patient folders will be created
base_dir = "patient_data"
os.makedirs(base_dir, exist_ok=True)

# Function to add a new patient
def add_new_patient(name, owner, phone, email, breed, birth_year):
    # Create a folder for the patient using the phone number and name
    patient_folder = os.path.join(base_dir, f"{phone}_{name}")
    os.makedirs(patient_folder, exist_ok=True)
    
    # Create subdirectories for bloodworks and reports
    bloodworks_dir = os.path.join(patient_folder, "bloodworks")
    os.makedirs(bloodworks_dir, exist_ok=True)
    
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

# Streamlit app
st.title("Vet Clinic Data Management")

# Sidebar for navigation
st.sidebar.title("Patients")

# Use st.session_state to store the current state
if "state" not in st.session_state:
    st.session_state.state = "Manage Patients"

# Create a button to toggle between states
if st.sidebar.button("Add New Patient"): 
    st.session_state.state = "Add New Patient"
    st.sidebar.markdown("### Add New Patient")

if st.session_state.state == "Add New Patient":
    new_patient_name = st.text_input("Name")
    new_patient_owner = st.text_input("Owner")
    new_patient_phone = st.text_input("Phone")
    new_patient_email = st.text_input("Email")
    new_patient_breed = st.text_input("Breed")
    new_patient_birth_year = st.number_input("Year of Birth", min_value=1900, max_value=2100, step=1)
    
    if st.button("Submit") :
        if new_patient_name and new_patient_owner and new_patient_phone and new_patient_email and new_patient_breed and new_patient_birth_year:
            patient_folder = add_new_patient(new_patient_name, new_patient_owner, new_patient_phone, new_patient_email, new_patient_breed, new_patient_birth_year)
            st.success(f"New patient '{new_patient_name}' created in folder: {patient_folder}")
            st.session_state.state = "Manage Patients"
        else: st.session_state.state = "Manage Patients"
if st.session_state.state == "Manage Patients":
    # State 2: Manage Patients
    st.sidebar.markdown("### Manage Patients")
    
    # Get a list of existing patients
    existing_patients = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]

    # Create a dynamic dropdown for selecting an existing patient
    selected_patient = st.sidebar.selectbox("Select a patient", existing_patients)

    # Check if a patient is selected
    if selected_patient:
        selected_patient_folder = [folder for folder in os.listdir(base_dir) if selected_patient in folder][0]
        selected_patient_data = pd.read_csv(os.path.join(base_dir, selected_patient_folder, "patient_info.csv"))

        # Display the selected patient's information in rows with columns
        st.title("General Information")
        st.write(selected_patient_data)

        # Bloodwork Section
        st.title("Bloodwork")
        # Additional code to manage bloodwork for this patient
        bloodwork_section = st.container()
        
        with bloodwork_section:
            st.subheader("Upload Bloodwork")
            bloodwork_file = st.file_uploader("Upload a PDF file", type=["pdf"])
            
            if bloodwork_file:
                # Save the uploaded bloodwork file to the patient's directory
                bloodwork_path = os.path.join(base_dir, selected_patient_folder, "bloodworks", bloodwork_file.name)
                with open(bloodwork_path, "wb") as f:
                    f.write(bloodwork_file.read())
                st.success(f"Bloodwork '{bloodwork_file.name}' uploaded successfully.")
            
            # List existing bloodwork files and display their content
            bloodwork_files = os.listdir(os.path.join(base_dir, selected_patient_folder, "bloodworks"))
            if bloodwork_files:
                st.subheader("Existing Bloodwork Files")
                for file in bloodwork_files:
                    st.write(file)
            else:
                st.info("No bloodwork files available.")

        # Reports Section
        st.title("Reports")
        # Additional code to manage reports for this patient
        report_section = st.container()
        
        with report_section:
            st.subheader("Upload Report")
            report_file = st.file_uploader("Upload a Report", type=["pdf"])
            
            if report_file:
                # Save the uploaded report file to the patient's directory
                report_path = os.path.join(base_dir, selected_patient_folder, "reports", report_file.name)
                with open(report_path, "wb") as f:
                    f.write(report_file.read())
                st.success(f"Report '{report_file.name}' uploaded successfully.")
            
            # List existing report files
            report_files = os.listdir(os.path.join(base_dir, selected_patient_folder, "reports"))
            if report_files:
                st.subheader("Existing Report Files")
                for file in report_files:
                    st.write(file)
            else:
                st.info("No report files available.")
