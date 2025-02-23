import streamlit as st
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
from torchvision import models
import torch.nn as nn
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_model(model_path):
    model = models.resnet18()
    model.fc = nn.Sequential(
        nn.Linear(512, 14),
        nn.Sigmoid()
    )
    checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model, checkpoint['pathology_list']

model, pathology_list = load_model('xray_classification_model.pth')

def preprocess_image(image):
    transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

st.title('Medical Image Report Analysis')

uploaded_file = st.file_uploader("Choose an X-ray image...", type=["jpg", "png"])

# Load and display the Lottie animation
lottie_animation = load_lottieurl("https://lottie.host/c0256f3b-9ae8-4876-b6f3-57cacf5549a9/yIsIRRwz3q.json")
st_lottie(lottie_animation, height=300, key="lottie")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded X-ray image.', use_column_width=True)
    
    processed_image = preprocess_image(image)
    
    with torch.no_grad():
        prediction = model(processed_image)
    
    predicted_classes = [pathology_list[i] for i, prob in enumerate(prediction[0]) if prob > 0.5]
    
    if predicted_classes:
        st.write("Predicted conditions:")
        for condition in predicted_classes:
            st.write(f"- {condition}")
    else:
        st.write("No conditions detected with high confidence.")

    st.write("Class Probabilities:")
    for i, (pathology, prob) in enumerate(zip(pathology_list, prediction[0])):
        st.write(f"{pathology}: {prob.item():.2f}")
