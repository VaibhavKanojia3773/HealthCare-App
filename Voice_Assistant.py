import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, TextClassificationPipeline
from streamlit_lottie import st_lottie

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the Lottie animation
lottie_animation = load_lottieurl("https://lottie.host/9e968fb7-8920-407e-bfb1-18e3dbb9054c/jn5LEXopae.json")



# Rest of your code remains the same
# Load CSS for styling
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load the pre-trained model and tokenizer
model_path = './fine_tune_bert'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = TFAutoModelForSequenceClassification.from_pretrained(model_path)

num_classes = 24  
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=num_classes)

# Initialize speech recognizer
r = sr.Recognizer()

# Function for text-to-speech
def speak(text):
    import threading
    def tts():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=tts).start()

# Function to record audio
def record_audio(language):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        st.write("Listening...")
        audio_text = ""
        while st.session_state.get('listening', False):  
            audio = r.listen(source)
            try:
                if language == 'Hindi':
                    audio_text = r.recognize_google(audio, language='hi-IN')
                else:
                    audio_text = r.recognize_google(audio, language='en-US')
                return audio_text
            except sr.RequestError as e:
                st.error("Could not request results; {0}".format(e))
            except sr.UnknownValueError:
                st.error("Unknown error occurred")
        return audio_text


st.title("Disease Prediction from Symptoms")
st.write("Choose the language for audio input:")
language = st.selectbox("Select Language:", ["English", "Hindi"])
# Display the Lottie animation
st_lottie(lottie_animation, height=300, key="lottie")

if st.button("Start Listening"):
    st.session_state['listening'] = True  

    if language == "Hindi":
        st.write("Please speak in Hindi.")
    else:
        st.write("Please speak in English.")
    
    audio_text = record_audio(language)

    if audio_text:
        st.write("Recognized Text:", audio_text)

        try:
            if language == "Hindi":
                translated_text = GoogleTranslator(source='hi', target='en').translate(audio_text)
            else:
                translated_text = audio_text
        except Exception as e:
            st.error(f"Translation error: {e}")
            translated_text = audio_text  

        st.write("Translated Text:", translated_text)

        # Prediction using the BERT model
        predictions = pipe(translated_text)

        if predictions and len(predictions) > 0:
            top_prediction = predictions[0][0]  
            predicted_disease = top_prediction['label']
            predicted_score = top_prediction['score']
            st.write(f"Predicted Disease: {predicted_disease} with score: {predicted_score:.2f}")
            speak(f"The predicted disease is {predicted_disease}.")
        else:
            st.write("No predictions were returned.")

if st.button("Stop Listening"):
    st.session_state['listening'] = False  
    st.write("Stopped listening.")
