import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables
load_dotenv()

# Function to get response from Gemini API
def get_gemini_response(question):
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=1)
    response = llm.invoke(question)
    return response

# Streamlit page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Custom styling
st.markdown("""
    <style>
        .stTextInput>div>div>input {border-radius: 10px; padding: 12px; border: 2px solid #4A90E2; font-size: 16px;}
        .stButton>button {background-color:rgb(33, 104, 185); color: white; font-size: 18px; padding: 10px 20px; border-radius: 10px;}
        .stButton>button:hover {background-color:rgb(23, 95, 166);}
        .stAlert {border-radius: 10px; font-size: 16px;}
    </style>
""", unsafe_allow_html=True)

# Page header with icon
st.title("🚀 AI-Powered Q&A")

# Input field with placeholder and icon
input_text = st.text_input("💬 Ask a question:", "", key="input")

# Button to submit the query with an icon
if st.button("✨ Get Answer"):
    if input_text.strip():
        with st.spinner("⏳ Generating response..."):
            response = get_gemini_response(input_text)
        st.subheader("🤖 Response:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a question before submitting.")