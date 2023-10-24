import os
import streamlit as st
import pandas as pd
from streamlit import session_state
import datetime
import manage_patients
import category_page
import new_patient
import main_page

# Default page
if not hasattr(session_state, 'current_page'):
    session_state.current_page = 'main_page'

def main():
    st.title('VetClinic App')

    # Check which page to display
    if session_state.current_page == 'main_page':
        main_page.main(session_state)
    elif session_state.current_page == 'manage_patients':
        manage_patients.main(session_state)
    elif session_state.current_page == 'category_page':
        category_page.main()
    elif session_state.current_page == 'new_patient':
        new_patient.main(session_state)

if __name__ == '__main__':
    main()

