from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader, PyMuPDFLoader
import streamlit as st
import tempfile  
import sys
print(sys.version)


# --- Page Configuration ---
st.set_page_config(page_title="Cold Email Generator", page_icon="📩")

# --- Page Title ---
st.title("📩 Cold Email Generator")
st.write("Generate a personalized cold email in seconds based on a job post and your resume.")

# --- Initialize LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,
)

# --- Load Job Post ---
def load_job_post(url):
    loader = WebBaseLoader(url)
    job_post_data = loader.load()
    return job_post_data[0].page_content if job_post_data else ""

# --- Load User CV ---
def load_user_cv(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())  
        temp_file_path = temp_file.name

    loader = PyMuPDFLoader(file_path=temp_file_path)
    cv_data = loader.load()
    return cv_data[0].page_content if cv_data else ""

# --- Prompt Template ---
template = """
You are an expert in persuasive communication and recruitment strategies. Your task is to generate a concise, engaging, and high-converting cold email for a job application.

### **Instructions:**  
Craft a **personalized** and **impactful** cold email based on the provided job posting and user resume. The email should be under **200 words** and follow a professional yet conversational tone.  

### **Email Structure:**  

1. **Subject Line:** Always formatted as **"Application for -Job Title- Role"** (e.g., "Application for Software Engineer Role").  
2. **Salutation:**  
   - If the hiring manager's name is available: **"Dear job poster name,"**  
   - Otherwise: **"Dear Hiring Manager,"**  
3. **Opening:** A compelling hook that establishes a connection or highlights a shared interest.  
4. **Body:** Align the candidate’s key skills and achievements with the job requirements in a persuasive yet natural way. If minor skill gaps exist, address them confidently with enthusiasm for learning.  
5. **Closing:** A clear call to action requesting a conversation or interview, along with a note of appreciation.  
6. **Signature:**  
   - **Best regards,**  
   - **Candidate Name**  
   - **Important Links: LinkedIn, Portfolio, etc.**  

### **Inputs:**  
- **Job Description:** {job_post}  
- **Candidate Resume:** {user_cv}  

### **Email:**  
Generate a **professional, personalized cold email** that:  
✅ Uses the correct **subject line format**  
✅ Starts with the **appropriate salutation**  
✅ Highlights the **most relevant skills and achievements**  
✅ Addresses any **minor skill gaps with confidence**  
✅ Ends with a **strong closing and signature**  

### **Additional Note:**  
- If the candidate is missing **must-have skills**, include a polite note **outside the email** only when applicable
- If only **nice-to-have** skills are missing, proceed with the email normally.  
"""

# --- User Inputs ---
job_post_url = st.text_input("🔗 Enter Job Post URL", placeholder="Paste the job post link here...")
user_cv = st.file_uploader("📄 Upload Your Resume (PDF)", type="pdf")

email_output = ""

if job_post_url and user_cv:
    if st.button("🚀 Generate Cold Email"):
        with st.spinner("✨ Generating your email..."):
            job_post_content = load_job_post(job_post_url)
            resume_content = load_user_cv(user_cv)

            # Generate email using LangChain
            prompt = PromptTemplate.from_template(template)
            chain = prompt | llm | StrOutputParser()
            email_output = chain.invoke({"job_post": job_post_content, "user_cv": resume_content})
            st.write(email_output)
