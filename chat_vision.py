from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, image):
    if image=="":
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
    elif input!="":
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input, image])
    else:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title='Gemini demo')
st.header("Gemini Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input = st.text_input("Input: ", key='input')
upload_file = st.file_uploader('Choose an image ...', type=['jpg', 'png', 'jpeg'])
image=''

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
else: image=''
submit = st.button("Chat")
if submit:
    response = get_gemini_response(input, image)
    st.subheader("Bot")
    st.write(response)