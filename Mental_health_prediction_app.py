import streamlit as st
import numpy as np
import pickle
import base64

# Set the page configuration with a mental health icon
st.set_page_config(
    page_title="Mental Health Assessment",
    page_icon="☘️",  
    layout="wide"
)

# Load the trained model
filename = "Mental_Health.sav"
loaded_model = pickle.load(open(filename, "rb"))

# Function to convert image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set the background image
def set_background_image(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;  /* Cover the entire background */
        background-position: center;  /* Center the image */
    }}
    .company-name {{
        position: absolute;
        bottom: 20px;  /* Position from the bottom */
        left: 50%;
        transform: translateX(-50%);  /* Center the text */
        color: white;  /* Text color */
        font-size: 24px;  /* Font size */
        font-weight: bold;  /* Font weight */
        text-align: center;  /* Center align text */
        background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent background for readability */
        padding: 10px;  /* Padding around the text */
        border-radius: 5px;  /* Rounded corners */
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the path to your local image
local_image_path = 'Mentalll.png'  # Ensure this path is correct

# Call the function to set the background
set_background_image(local_image_path)

# Add CSS for input fields and text color
st.markdown("""
    <style>
        .stTextInput, .stSelectbox, .stNumberInput {
            border: 2px solid #4CAF50; /* Green border */
            border-radius: 5px; /* Rounded corners */
            padding: 10px; /* Padding inside the input */
            font-size: 16px; /* Font size */
            color: #000000; /* Very dark color for inputs */
        }
        /* Set text color for various Streamlit components */
        h1, h2, h3, p, label {
            color: #000000; /* Very dark color */
        }
        .stButton, .stMarkdown, .stText {
            color: #000000; /* Very dark color */
        }
        /* Set light blue color for resources and links */
        .resource-link {
            color: #ADD8E6; /* Light blue color for links */
        }
    </style>
""", unsafe_allow_html=True)

# Define the main function for Streamlit
def main():
    # Set up the Streamlit title and description
    st.markdown("<h1 style='color: green; text-align: center; font-size: 40px; font-family: Arial, sans-serif;'>Mental Health Assessment</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; font-size: 18px; color: #000000;'>A predictive tool that assesses workplace and personal factors to identify individuals potentially at risk, enabling timely mental health support.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line for separation

    # Create a two-column layout for inputs and descriptions
    col1, col2 = st.columns(2)
    with col1:
        # Input fields for each feature
        Age = st.number_input("Age", min_value=18, max_value=100, value=30, help="Enter your age.")
        Gender = st.selectbox("Gender", ["Female", "Male", "Other"], help="Select your gender.")
        family_history = st.selectbox("Do you have a family history of mental health issues?", ["No", "Yes"], help="Family history of mental illness?")
        work_interfere = st.selectbox("How much does mental health interfere with your work?", ["Never", "Often", "Rarely", "Sometimes"], help="Work interfere?")
        remote_work = st.selectbox("Do you work remotely?", ["No", "Yes"], help="Remote work?")
        benefits = st.selectbox("Does your workplace offer mental health benefits?", ["Don't know", "No", "Yes"], help="Mental Health Benefits")
        care_options = st.selectbox("Are mental health care options available at your workplace?", ["Not sure", "Yes", "No"], help="Care options available?")
        supervisor = st.selectbox("Have you discussed mental health issues with your supervisor?", ["No", "Some of them", "Yes"], help="Supervisor or your Boss")
        mental_vs_physical = st.selectbox("Do you believe mental health is as important as physical health?", ["Don't know", "No", "Yes"], help="Mental health as important as physical health?")

        # Prediction button
        if st.button("Predict", key="predict_button"):
            # Store inputs in the correct order for the model
            input_data = [
                Age,
                float(Gender == "Female"), float(Gender == "Male"), float(Gender == "Other"),
                float(family_history == "No"), float(family_history == "Yes"),
                float(work_interfere == "Never"), float(work_interfere == "Often"),
                float(work_interfere == "Rarely"), float(work_interfere == "Sometimes"),
                float(remote_work == "No"), float(remote_work == "Yes"),
                float(benefits == "Don't know"), float(benefits == "No"),
                float(benefits == "Yes"), float(care_options == "No"),
                float(care_options == "Not sure"), float(care_options == "Yes"),
                float(supervisor == "No"), float(supervisor == "Some of them"),
                float(supervisor == "Yes"), float(mental_vs_physical == "No"),
                float(mental_vs_physical == "Don't know"), float(mental_vs_physical == "Yes")
            ]
            input_data_as_numpy_array = np.asarray(input_data)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

            # Make prediction
            prediction = loaded_model.predict(input_data_reshaped)
            prediction_probabilities = loaded_model.predict_proba(input_data_reshaped)

            # Display results
            if prediction[0] == 0:
                st.write("<p style='color: #000000;'>Unlikely to seek mental health treatment</p>", unsafe_allow_html=True)
            else:
                st.write("<p style='color: #000000;'>Likely to seek mental health treatment</p>", unsafe_allow_html=True)

            # Display prediction probabilities
            st.write("<p style='color: #000000;'>Prediction Probabilities:</p>", unsafe_allow_html=True)
            st.write(f"<p style='color: #000000;'>Unlikely: {prediction_probabilities[0][0]:.2f}</p>", unsafe_allow_html=True)
            st.write(f"<p style='color: #000000;'>Likely: {prediction_probabilities[0][1]:.2f}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color: #000000;'>Resources</h3>", unsafe_allow_html=True)
        st.write("<p style='color: #000000;'>If you or someone you know is struggling with mental health, please reach out to a professional. Remember, you are not alone.</p>", unsafe_allow_html=True)
        st.write("<p style='color: #000000;'>Here are some resources:</p>", unsafe_allow_html=True)
        st.write("<ul>", unsafe_allow_html=True)
        st.write(f"<li><a href='https://suicidepreventionlifeline.org/' class='resource-link'>National Suicide Prevention Lifeline</a></li>", unsafe_allow_html=True)
        st.write(f"<li><a href='https://988lifeline.org/' class='resource-link'>988 Suicide & Crisis Lifeline</a></li>", unsafe_allow_html=True)
        st.write(f"<li><a href='https://www.mhanational.org/' class='resource-link'>Mental Health America</a></li>", unsafe_allow_html=True)
        st.write(f"<li><a href='https://nami.org/' class='resource-link'>NAMI</a></li>", unsafe_allow_html=True)
        st.write("</ul>", unsafe_allow_html=True)

    # Footer
    st.markdown("<footer style='text-align: center; padding: 20px; color: #777;'>© 2023 Nurtura | A Haven of Understanding and Comfort.</footer>", unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()