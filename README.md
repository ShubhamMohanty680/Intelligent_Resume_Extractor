# 📄 Intelligent Resume Extractor

An **AI-powered Resume Intelligence & Filtering system** that converts unstructured resumes into structured, recruiter-ready data using **LangChain**, **Google Gemini**, and **Streamlit**.

Upload a ZIP file containing multiple resumes (PDF/DOCX), automatically extract key candidate details, and download the results as a **CSV file** for easy screening and analysis.

---

## 🚀 Features

- 📦 Upload a ZIP file containing multiple resumes  
- 📄 Supports PDF and DOCX resume formats  
- 🤖 Uses Generative AI to understand resume content  
- 📊 Extracts structured information:
  - Candidate Name  
  - Professional Summary  
  - Years of Experience  
  - Skills  
  - Important Links (GitHub, LinkedIn, Portfolio, etc.)  
- 📥 Download extracted data as a CSV file  
- 🎨 Modern and interactive UI built with Streamlit  

---

## 🧠 Why This Project?

Recruiters and HR teams often receive resumes in bulk, making manual screening:
- Time-consuming  
- Inconsistent  
- Error-prone  

This project automates resume understanding and transforms **unstructured documents into structured intelligence**, enabling faster and smarter hiring decisions.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Web application UI  
- **LangChain** – LLM orchestration  
- **Google Gemini (Generative AI)** – Resume understanding  
- **TypedDict Structured Output** – Schema-enforced extraction  
- **PyMuPDF** – PDF text extraction  
- **Pandas** – CSV generation  
- **Zipfile & OS** – Bulk resume handling  

---

## 📂 Project Workflow

1. User uploads a ZIP file containing resumes  
2. Each resume is read and converted into raw text  
3. LLM extracts structured data using a fixed schema  
4. All extracted data is aggregated into a CSV file  
5. User downloads the CSV for filtering and analysis  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ShubhamMohanty680/Intelligent_Resume_Extractor.git
cd intelligent-resume-extractor
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On MAC: source venv/bin/activate 
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Set Environment Variables (Create a .env file and add)
```bash
GOOGLE_API_KEY=your_gemini_api_key
```
### 5️⃣ Run the Application
```bash
streamlit run app.py
```



