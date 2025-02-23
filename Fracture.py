import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from torchvision import models
import requests
from streamlit_lottie import st_lottie


# Define the model architecture
class ConvolutionalNetwork(torch.nn.Module):
    def __init__(self):
        super(ConvolutionalNetwork, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 6, 3, 1)
        self.conv2 = torch.nn.Conv2d(6, 16, 3, 1)
        self.fc1 = torch.nn.Linear(16 * 54 * 54, 120)
        self.fc2 = torch.nn.Linear(120, 84)
        self.fc3 = torch.nn.Linear(84, 20)
        self.fc4 = torch.nn.Linear(20, 2)  # 2 classes: fractured and not fractured

    def forward(self, X):
        X = torch.nn.functional.relu(self.conv1(X))
        X = torch.nn.functional.max_pool2d(X, 2, 2)
        X = torch.nn.functional.relu(self.conv2(X))
        X = torch.nn.functional.max_pool2d(X, 2, 2)
        X = X.view(-1, 16 * 54 * 54)
        X = torch.nn.functional.relu(self.fc1(X))
        X = torch.nn.functional.relu(self.fc2(X))
        X = torch.nn.functional.relu(self.fc3(X))
        X = self.fc4(X)
        return torch.nn.functional.log_softmax(X, dim=1)

# Load the trained model
model = ConvolutionalNetwork()
model.load_state_dict(torch.load('fracture_detection_model.pth'))
model.eval()

# Define image transformation
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



# Streamlit app
st.title('Fracture Report Analysis')

# Load and display the Lottie animation
lottie_animation = load_lottieurl("https://lottie.host/436054af-5a85-4bc2-995b-00536cb1dc95/8WOmCvst0l.json")
st_lottie(lottie_animation, height=300, key="lottie")

uploaded_file = st.file_uploader("Choose an X-ray image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded X-ray Image', use_column_width=True)
    
    # Preprocess the image
    input_tensor = transform(image).unsqueeze(0)
    
    # Make prediction
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.exp(output)
        predicted_class = torch.argmax(probabilities, dim=1).item()
    
    # Display result
    class_names = ['Fractured', 'Not Fractured']
    st.write(f"Prediction: {class_names[predicted_class]}")
    st.write(f"Confidence: {probabilities[0][predicted_class]:.2f}")

