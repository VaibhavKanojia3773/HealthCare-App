import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_health = load_lottieurl("https://lottie.host/bd72a99e-f3b0-4de7-9947-6b9ba18d2a14/aNyI7323dB.json")
lottie_check = load_lottieurl("https://lottie.host/bd2a2c37-30ac-4e04-a56a-5a9acfd0bfa3/EV9OYEiLwI.json")

# Load datasets
description = pd.read_csv(r'Database/description.csv')
precautions = pd.read_csv(r'Database/precautions_df.csv')
medications = pd.read_csv(r'Database/medications.csv')
diets = pd.read_csv(r'Database/diets.csv')

# Get list of unique diseases
diseases = description['Disease'].unique().tolist()

# Page title with animation
st.title("Tailored Suggestion")
st_lottie(lottie_health, height=200)

# Dropdown for disease selection
selected_disease = st.selectbox("Select a disease:", ["Select"] + diseases)

# Button for confirmation
if st.button("Enter"):
    if selected_disease != "Select":
        # Display disease information
        st.header(f"Information for {selected_disease}")

        # Description section with styling
        st.subheader("Description")
        desc = description[description['Disease'] == selected_disease]['Description'].values[0]
        st.markdown(
            f"<div style='padding:10px; background-color:#f0f8ff; border-radius:10px; font-size:18px; color:#333;'>{desc}</div>",
            unsafe_allow_html=True,
        )

        # Precautions section (remove disease name row and index)
        st.subheader("Precautions")
        precs = precautions[precautions['Disease'] == selected_disease].iloc[:, 1:].values.flatten()[1:]  # Skip first row (disease name)
        precs_table = pd.DataFrame({"Precaution": precs})
        st.markdown(precs_table.to_html(index=False), unsafe_allow_html=True)  # Display without index

        # Medications section (without index)
        st.subheader("Medications")
        meds_row = medications[medications['Disease'] == selected_disease]['Medication']
        if meds_row.empty:
            st.warning("No medications found for the selected disease.")
        else:
            meds_list = eval(meds_row.values[0])  # Convert string representation of list to actual list
            meds_table = pd.DataFrame({"Medication": meds_list})
            st.markdown(meds_table.to_html(index=False), unsafe_allow_html=True)  # Display without index

        # Diets section (without index)
        st.subheader("Recommended Diet")
        diet_row = diets[diets['Disease'] == selected_disease]['Diet']
        if diet_row.empty:
            st.warning("No diet recommendations found for the selected disease.")
        else:
            diet_list = eval(diet_row.values[0])
            diet_table = pd.DataFrame({"Diet": diet_list})
            st.markdown(diet_table.to_html(index=False), unsafe_allow_html=True)  # Display without index

    else:
        # Warning message if no disease is selected
        st.warning("Please select a valid disease.")
else:
    # Display an animation encouraging the user to select a disease
    st_lottie(lottie_check, height=200)
    st.markdown(
        "<p style='font-size:18px; color:#555;'>Use the dropdown above to select a disease and click <b>Enter</b> to get tailored suggestions.</p>",
        unsafe_allow_html=True,
    )
