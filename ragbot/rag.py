import os
# import warnings
# import logging
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# warnings.filterwarnings("ignore")
# logging.getLogger("transformers").setLevel(logging.ERROR)

st.title("RAG CHATBOT")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message['content'])

prompt = st.chat_input("pass your prompt here!")

if prompt:
   st.chat_message("user").markdown(prompt)
   st.session_state.messages.append({"role":"user", "content": prompt})

   gemini_sys_prompt = ChatPromptTemplate.from_template(
                       """You are very smart at everything, you always give the best, 
                            the most accurate and most precise answers. Answer the following Question: {user_prompt}.
                            Start the answer directly. No small talk please"""
                    )
    
   gemini_chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.6, gemini_api_key=os.getenv("GOOGLE_API_KEY"))
   chain = gemini_sys_prompt | gemini_chat | StrOutputParser()
   response = chain.invoke({"user_prompt": prompt})
   st.chat_message("assistant").markdown(response)
   st.session_state.messages.append({"role":"assistant", 'content':response})
