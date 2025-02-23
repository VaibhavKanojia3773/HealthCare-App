import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import tensorflow as tf
import requests
from streamlit_lottie import st_lottie

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the trained model
model = load_model('CNN_model.h5')

# Define image size and other parameters (matching the preprocessing done in training)
img_width, img_height = 256, 256

# Preprocessing the uploaded image
def preprocess_image(img):
    img = img.resize((img_width, img_height))
    img_array = np.array(img)
    if img_array.shape[-1] != 3:
        img_array = np.stack([img_array] * 3, axis=-1)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 256.0
    return img_array

# Prediction function
def predict_image(img):
    img_array = preprocess_image(img)
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5:
        return 'Normal', prediction[0][0]
    else:
        return 'Pneumonia', 1 - prediction[0][0]

# Streamlit app interface
def main():
    st.title("Pneumonia Detection from X-ray Images")
    
    # Load and display the Lottie animation
    lottie_animation = load_lottieurl("https://lottie.host/dac99abf-501c-4b13-b7c5-22a1f49b65a0/DnXkMHxu8C.json")
    st_lottie(lottie_animation, height=300, key="lottie")
    
    st.write("Upload an X-ray image to detect if it is Normal or has Pneumonia.")
    
    uploaded_file = st.file_uploader("Choose an X-ray image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded X-ray Image", use_column_width=True)
        
        result, confidence = predict_image(img)
        
        st.write(f"Prediction: **{result}** with confidence: {confidence*100:.2f}%")

# Run the Streamlit app
if __name__ == "__main__":
    main()
