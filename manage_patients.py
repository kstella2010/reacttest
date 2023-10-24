import os
import streamlit as st
import pandas as pd
from streamlit import session_state
from datetime import datetime
                
def main(session_state):
    # Define the base directory where patient folders will be created
    base_dir = "patient_data"
    os.makedirs(base_dir, exist_ok=True)

    st.title("Manage Patient")

    # Sidebar for navigation
    st.sidebar.title("Patients")

    # Create a button to toggle between states
    if st.sidebar.button("Add New Patient"): 
        session_state.current_page = 'new_patient'
   
    # Get a list of existing patients
    existing_patients = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]

    # Create a dynamic dropdown for selecting an existing patient
    selected_patient = st.sidebar.selectbox("Select a patient", existing_patients)

    # Check if a patient is selected
    if selected_patient:
        selected_patient_folder = [folder for folder in os.listdir(base_dir) if selected_patient in folder][0]
        selected_patient_data = pd.read_csv(os.path.join(base_dir, selected_patient_folder, "patient_info.csv"))
        selected_patient_path = os.path.join(base_dir, selected_patient_folder)

        # Display the selected patient's information in rows with columns
        st.title("General Information")
        st.write(selected_patient_data)

        ## New category button
        if st.button("Add New Category"):
        # Redirect to the Category Page by setting a query parameter
            session_state.current_page = 'category_page'

        category_section = st.container()

        # Loop through categories inside the selected patient's folder
        for category_dir in os.listdir(selected_patient_path):
            category_path = os.path.join(selected_patient_path, category_dir)
            if os.path.isdir(category_path):
                # Extract category_name and category_date from the directory name
                category_parts = category_dir.split("_")
                category_name = "_".join(category_parts[:-1])
                category_date = category_parts[-1]

                with category_section:
                    st.subheader(category_name)  # Display category name as a title
                    st.write(f"Date: {category_date}")  # Display category date as a subtitle

                    # Display Reports and Treatment subcategories
                    reports_path = os.path.join(category_path, "reports")
                    treatment_path = os.path.join(category_path, "treatment")

                    # Assuming you want buttons or links to view these folders:
                    if os.path.exists(reports_path):
                        st.text("Upload File")
                        report_file = st.file_uploader(f"Upload a PDF file for {category_name}", type=["pdf"], key=f"uploader_{category_name}")
                        
                        if report_file:
                            # Save the uploaded bloodwork file to the patient's directory
                            file_path = os.path.join(category_path,"reports", report_file.name)
                            with open(file_path, "wb") as f:
                                f.write(report_file.read())
                            st.success(f"File '{report_file.name}' uploaded successfully.")
                        
                        # List existing bloodwork files and display their content
                        category_files = os.listdir(os.path.join(category_path,"reports"))
                        if category_files:
                            st.text("Existing Files")
                            for file in category_files:
                                st.write(file)
                        else:
                            st.info("No files available.")
                    if os.path.exists(treatment_path):
                        st.subheader("Treatment")
    
                        treatment_text = st.text_input(f"Treatment input for {category_name}",key=f"txt_{category_name}")
                        
                        # Check if treatment text is not empty
                        if treatment_text:
                            # Get the filename from the first few words of the treatment text
                            filename = "_".join(treatment_text.split()[:3]) + ".txt"
                            file_path = os.path.join(treatment_path, filename)
                            
                            # Save the treatment text to a .txt file inside the treatments directory
                            with open(file_path, "w") as f:
                                f.write(treatment_text)
                            st.success(f"Saved treatment as {filename}")

                        st.text("Previous Treatments")
                        
                        # List all .txt files inside the treatments directory
                        treatment_files = [f for f in os.listdir(treatment_path) if f.endswith(".txt")]
                        
                        if treatment_files:
                            for file in treatment_files:
                                # Get the file's last modified date
                                file_date = datetime.fromtimestamp(os.path.getmtime(os.path.join(treatment_path, file))).strftime('%Y-%m-%d')
                                with open(os.path.join(treatment_path, file), 'r') as f:
                                    content = f.read()
                                    st.write(f"Date: {file_date}")
                                    st.write(content)
                        else:
                            st.info("No treatments available.")
                                            
                                        
                            

