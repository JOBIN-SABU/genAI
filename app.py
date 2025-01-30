import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Set the page configuration
st.set_page_config(
    page_title="GeminiDecode: Multilanguage Document Extraction by Gemini Pro",
    page_icon=":page_facing_up:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
load_dotenv(dotenv_path="google.env")

# Get the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Configure Google Gemini API
genai.configure(api_key=api_key)

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image, prompt])
    return response.text

# Streamlit app
st.header("GeminiDecode: Multilanguage Document Extraction by Gemini Pro")
text = (
    "Utilizing Gemini Pro AI, this project effortlessly extracts vital information "
    "from diverse multilingual documents, transcending language barriers with "
    "precision and efficiency for enhanced productivity and decision-making."
)
styled_text = f"<span style='font-family: serif;'>{text}</span>"
st.markdown(styled_text, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose an image of the document:", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Input prompt
input_prompt = """
You are an expert in understanding invoices.
We will upload an image as an invoice and you will have to answer any question based on the uploaded invoice image.
"""

# Submit button
submit = st.button("Tell me about the document")

# If submit button is clicked
if submit and image is not None:
    response = get_gemini_response(input_prompt, image, input_prompt)
    st.subheader("The response is")
    st.write(response)
