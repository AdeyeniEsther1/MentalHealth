import streamlit as st
import numpy as np
import pickle
import base64

# Set the page configuration with a mental health icon
st.set_page_config(
    page_title="Mental Health Risk Assessment",
    page_icon="☘️",  # You can use an emoji or a path to an image file
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

# Add CSS for input fields
st.markdown("""
    <style>
        .stTextInput, .stSelectbox, .stNumberInput {
            border: 2px solid #4CAF50; /* Green border */
            border-radius: 5px; /* Rounded corners */
            padding: 10px; /* Padding inside the input */
            font-size: 16px; /* Font size */
        }
    </style>
""", unsafe_allow_html=True)

# Define the main function for Streamlit
def main():
    # Set up the Streamlit title and description
    st.markdown("<h1 style='color: green; text-align: center; font-size: 40px; font-family: Arial, sans-serif;'>Mental Health Risk Assessment</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; font-size: 18px; color: #555;'>A predictive tool that assesses workplace and personal factors to identify individuals potentially at risk, enabling timely mental health support.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line for separation

    # Create a two-column layout for inputs and descriptions
    # Create a two-column layout for inputs and descriptions
    col1, col2 = st.columns(2)
    with col1:
        # Input fields for each feature
        Age = st.number_input("Age", min_value=18, max_value=100, value=30, help="Enter your age.")
        Gender = st.selectbox("Gender", ["Female", "Male", "Other"], help="Select your gender.")
        family_history = st.selectbox("Family history of mental illness?", ["No", "Yes"], help="Do you have a family history of mental health issues?")
        work_interfere = st.selectbox("Work interfere", ["Never", "Often", "Rarely", "Sometimes"], help="How much does mental health interfere with your work?")
        remote_work = st.selectbox("Remote work?", ["No", "Yes"], help="Do you work remotely?")
        benefits = st.selectbox("Benefits", ["Don't know", "No", "Yes"], help="Does your workplace offer mental health benefits?")
        care_options = st.selectbox("Care options available?", ["Not sure", "Yes", "No"], help="Are mental health care options available at your workplace?")
        supervisor = st.selectbox("Supervisor", ["No", "Some of them", "Yes"], help="Have you discussed mental health issues with your supervisor?")
        mental_vs_physical = st.selectbox("Mental health as important as physical health?", ["Don't know", "No", "Yes"], help="Do you believe mental health is as important as physical health?")

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
                st.write("Unlikely to seek mental health treatment")
            else:
                st.write("Likely to seek mental health treatment")

            # Display prediction probabilities
            st.write("Prediction Probabilities:")
            st.write(f"Unlikely: {prediction_probabilities[0][0]:.2f}")
            st.write(f"Likely: {prediction_probabilities[0][1]:.2f}")

    with col2:
        st.markdown("<h3 style='color: blue;'>Resources</h3>", unsafe_allow_html=True)
        st.write("If you or someone you know is struggling with mental health, please reach out to a professional. Remember, you are not alone.")
        st.write("Here are some resources:")
        st.write("- [National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/)")
        st.write("- [988 Suicide & Crisis Lifeline](https://988lifeline.org/)")
        st.write("- [Mental Health America](https://www.mhanational.org/)")
        st.write("- [NAMI](https://nami.org/)")

    # Footer
    st.markdown("<footer style='text-align: center; padding: 20px; color: #777;'>© 2023 Nurtura | A Haven of Understanding and Comfort.</footer>", unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()