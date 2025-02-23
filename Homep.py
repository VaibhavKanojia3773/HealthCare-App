import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Set page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Dr. Buddy 🩺",
    page_icon=":smile:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_doctor = load_lottieurl("https://lottie.host/f5946b5c-43a6-4040-919e-58687cc4b184/caFOC576ht.json")
lottie_ai = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tutvdkg0.json")
lottie_new_animation = load_lottieurl("https://lottie.host/bc37c4bc-345a-49f1-8611-857868709bc0/TtETUs5MIX.json")

# Inject custom CSS for sidebar and page styling
st.markdown(
    """
    <style>
    /* Sidebar container styling */
    [data-testid="stSidebar"] {
        background-color: #2c2f33;
        color: white;
        font-family: 'Arial', sans-serif;
        padding: 20px;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        font-size: 24px;
        font-weight: bold;
        color: #7289da;
        margin-bottom: 20px;
    }

    /* Sidebar links styling */
    [data-testid="stSidebar"] .css-1v3fvcr a {
        color: #ffffff !important;
        font-size: 45px;
        text-decoration: none;
        padding: 10px 15px;
        display: block;
        border-radius: 5px;
        transition: all 0.3s ease-in-out;
    }

    /* Hover effect for links */
    [data-testid="stSidebar"] .css-1v3fvcr a:hover {
        background-color: #7289da;
        color: white !important;
        transform: scale(1.05);
    }

    /* Sidebar navigation options */
    [data-testid="stSidebar"] .streamlit-radio {
        font-size: 45px !important;
    }

    /* Custom bullet style for sidebar options */
    [data-testid="stSidebar"] .streamlit-radio label::before {
        content: '🔹';
        margin-right: 10px;
        color: #7289da;
    }

    /* General body styling */
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #1E1E2F;
        color: #FFFFFF;
        font-size: 50px;
    }

    /* Title styling */
    .title {
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        font-family: 'Poppins', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        margin-top: -50px; /* Reduce unwanted space above the title */
    }

    /* Subtitle styling */
    .subtitle {
        font-size: 50px;
        text-align: center;
        color: #BBBBBB;
        margin-bottom: 40px;
    }

    /* Feature cards styling */
    .feature-card {
        background-color: #FFFFFF; 
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        align-items: center; 
        justify-content: center; 
    }
    
    .feature-title {
        font-size: 20px;
        font-weight: bold;
        color: #003366; /* Dark Blue Color */
        text-align: center; 
    }

    /* Update paragraph text color inside feature cards */
    .feature-card p {
        font-size: 16px; 
        color: #333333; /* Dark Gray Color for better visibility */
        text-align: center;
    }

    /* Increase font size for main content */
    .main-content {
        font-size: 75px;
    }

    /* Increase font size for section headers */
    .section-header {
        font-size: 28px;
        font-weight: bold;
        color: #4A90E2;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation with material icons
selected_page = st.sidebar.radio(
    "Go to",
    options=[
        "Home 🏠",
        "Voice Assistant 🎙️",
        "Fracture 🦴",
        "Pneumonia 🫁",
        "Report Analysis 📝",
        "Tailored Suggestion 🎯",  # Add this new option
    ],
)


# Page navigation logic
if selected_page == "Home 🏠":
    
    # Main content for Home page
    st.markdown("<h1 class='title'>Dr. Buddy 🩺</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Empowering Healthcare with AI</p>", unsafe_allow_html=True)

    # Add Lottie animation at the top
    st_lottie(lottie_doctor, height=300)

    # About Section
    st.markdown("<h3 class='section-header'>About Dr. Buddy</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st_lottie(lottie_new_animation, height=200)

    with col2:
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.write("""
            Dr. Buddy is an AI-powered medical assistant designed to revolutionize healthcare.
            
            - Provides real-time voice interaction for seamless communication.
            - Analyzes medical reports using cutting-edge computer vision techniques.
            - Offers intelligent decision support to assist healthcare professionals.
            
            No more tedious paperwork or time-consuming diagnosis. Dr. Buddy is here to help.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Feature cards section
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='feature-card'><h3 class='feature-title'>🗣️ Voice Interaction</h3><p>Real-time conversations powered by advanced NLP.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><h3 class='feature-title'>🔬 Medical Report Analysis</h3><p>Accurate insights using computer vision and CNNs.</p></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='feature-card'><h3 class='feature-title'>🧠 Intelligent Decision Support</h3><p>AI-driven recommendations for healthcare professionals.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><h3 class='feature-title'>🔄 Continuous Learning</h3><p>Constantly improving with new medical data.</p></div>", unsafe_allow_html=True)


    # Additional Section with Animation
    st.markdown("<h3 class='section-header'>How AI is Transforming Healthcare</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.write("""
            Artificial Intelligence (AI) is transforming the healthcare industry by enabling faster diagnoses,
            personalized treatment plans, and improved patient outcomes.

            Key benefits of AI in healthcare:

              - Faster diagnosis and treatment.
              - Reduced human error in medical decisions.
              - Enhanced patient care and satisfaction.
            """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st_lottie(lottie_ai, height=250)
        


elif selected_page == "Fracture 🦴":
   with open("pages/Fracture.py") as f:
       exec(f.read())

elif selected_page == "Pneumonia 🫁":
   with open("pages/Pneumonia.py") as f:
       exec(f.read())

elif selected_page == "Voice Assistant 🎙️":
   with open("pages/Voice_Assistant.py") as f:
       exec(f.read())

elif selected_page == "Report Analysis 📝":
   with open("pages/XM.py") as f:
       exec(f.read())
elif selected_page == "Tailored Suggestion 🎯":
   with open("pages\sugestions.py") as f:
       exec(f.read())


# Footer Section (common across all pages)
st.markdown("---")
st.markdown("""
<div style="text-align:center;">
   <p style="font-size:16px;">© 2025 Dr. Buddy | Empowering Healthcare with AI</p>
</div>
""", unsafe_allow_html=True)
