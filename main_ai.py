import streamlit as st 
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import pymupdf
import zipfile
from typing import TypedDict, Annotated
import pandas as pd
import shutil

st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="wide")

# --- CUSTOM CSS & STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2c3e50;
        text-align: center;
        padding: 20px;
        font-weight: 800;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Card-like container for the uploader */
    .upload-card {
        background: rgba(255, 255, 255, 0.7);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 25px;
    }
    
    /* Button Styling */
    div.stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)


load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

st.markdown('<h1 class="main-header">📄 Resume Intelligence Extractor</h1>', unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop your ZIP file containing PDF resumes here", type="zip")
    st.markdown('</div>', unsafe_allow_html=True)
    
    submit_clicked = st.button("Process Resumes")

class ExtractText(TypedDict):
    name: Annotated[str, "Extract the Name of the candidate from the resume"]
    summary: Annotated[str, "Extract only the Summary of the resume provided not extract the phone number or email or github links"]
    exp: Annotated[int, "Extract the experience mentioned in the resume if present else return 0"]
    skills: Annotated[list[str], "Extract the skills from the resume"]
    links: Annotated[list[str], "Extract the links from the resume as list of strings"]


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite") # Updated to current flash model
llm = model.with_structured_output(ExtractText)
EXTRACT_DIR = "extracted_pdfs"

if submit_clicked:
    if uploaded_file:
        with st.status("Analyzing Resumes...", expanded=True) as status:
            extracted_data = []
            if os.path.exists(EXTRACT_DIR):
                shutil.rmtree(EXTRACT_DIR)
            os.makedirs(EXTRACT_DIR)
            
            with zipfile.ZipFile(uploaded_file, 'r') as zip_f:
                zip_f.extractall(EXTRACT_DIR)
                files_list = [f for f in os.listdir(EXTRACT_DIR) if f.endswith(".pdf") or f.endswith(".docx")]
                
                for files in files_list:
                    st.write(f"Processing: `{files}`")
                    doc = pymupdf.open(os.path.join(EXTRACT_DIR, files))
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    doc.close()
                    
                    response = llm.invoke(text)
                    
                    extracted_info = {
                        "Name": response['name'], 
                        "Summary": response['summary'],
                        "Experience (Yrs)": response['exp'],
                        "Skills": ", ".join(response['skills']),
                        "Links": ", ".join(response['links'])
                    }
                    extracted_data.append(extracted_info)
            
            status.update(label="Extraction Complete!", state="complete", expanded=False)

        if extracted_data: 
            df = pd.DataFrame(extracted_data) 
            
            # st.success(f"Successfully processed {len(extracted_data)} resumes!")
            
            # Displaying a preview of the data
            # with st.expander(" Preview Extracted Data"):
            #     st.dataframe(df, use_container_width=True)
            
            # Modern Download Button
            st.download_button(
                label="📥 Download Results as CSV",
                data=df.to_csv(index=False),
                file_name="extracted_resumes.csv",
                mime="text/csv"
            )
    else:
        st.error("Please upload a ZIP file first.")