import streamlit as st

# Title for your app
st.title("My Streamlit App")

# Add some text
st.write("Welcome to my Streamlit app!")

# Add a sidebar
st.sidebar.title("Sidebar")

# Add a slider widget
slider_value = st.slider("Select a value", 0, 100, 50)

# Display the selected value
st.write(f"You selected: {slider_value}")
