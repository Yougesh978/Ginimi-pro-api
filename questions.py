from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get responses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Yogi's Gemini chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input: ", key="input")
submit_button = st.button("Ask the question")

if submit_button and input_text:
    # Prompt the model with a clearer instruction
    prompt = "Generate 10 similar questions related to: " + input_text
    response = get_gemini_response(prompt)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
