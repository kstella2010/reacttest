import os
import streamlit as st
import pandas as pd

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
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Select an Option", ("Home", "Add Patient", "Manage Patients"))

if selected_option == "Home":
    st.write("Welcome to the Vet Clinic Data Management System!")

elif selected_option == "Add Patient":
    st.sidebar.title("Add New Patient")
    
    new_patient_name = st.sidebar.text_input("Name")
    new_patient_owner = st.sidebar.text_input("Owner")
    new_patient_phone = st.sidebar.text_input("Phone")
    new_patient_email = st.sidebar.text_input("Email")
    new_patient_breed = st.sidebar.text_input("Breed")
    new_patient_birth_year = st.sidebar.number_input("Year of Birth", min_value=1900, max_value=2100, step=1)
    
    if st.sidebar.button("Create New Patient"):
        if new_patient_name and new_patient_owner and new_patient_phone and new_patient_email and new_patient_breed and new_patient_birth_year:
            patient_folder = add_new_patient(new_patient_name, new_patient_owner, new_patient_phone, new_patient_email, new_patient_breed, new_patient_birth_year)
            st.sidebar.success(f"New patient '{new_patient_name}' created in folder: {patient_folder}")
        else:
            st.sidebar.warning("Please fill in all patient information.")

elif selected_option == "Manage Patients":
    st.sidebar.title("Manage Patients")
    
    # Search by name or phone
    search_query = st.sidebar.text_input("Search by Name or Phone")
    
    if search_query:
        # Create a list to store search results
        search_results = []
        
        # Loop through patient folders and check if the search query matches name or phone
        for patient_folder in os.listdir(base_dir):
            patient_info_csv = os.path.join(base_dir, patient_folder, "patient_info.csv")
            if os.path.exists(patient_info_csv):
                patient_info = pd.read_csv(patient_info_csv)
                if any(patient_info["Name"].str.contains(search_query, case=False)) or search_query in patient_info["Phone"].values:
                    search_results.append(patient_info)
        
        # Display search results
        if search_results:
            st.sidebar.success(f"Search results for '{search_query}':")
            for idx, result in enumerate(search_results, start=1):
                st.sidebar.write(f"{idx}. {result['Name'].values[0]} ({result['Phone'].values[0]})")
        else:
            st.sidebar.warning("No matching patients found.")

    st.markdown("### General Patient Information")
    
    # Code to display and update general patient information
    # ...
    
    st.markdown("### Bloodworks")
    
    # Code to display and manage bloodwork PDFs
    # ...
    
    st.markdown("### Reports")
    
    # Code to display and manage reports PDFs
    # ...

