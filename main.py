# Set up Groq client and page configuration firstimport streamlit as st
import streamlit as st
import PyPDF2
import io
from groq import Groq
from datetime import datetime

# Set page configuration - MUST BE FIRST
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up Groq client
client = Groq(
    api_key= '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'
)

# Custom CSS with modern design
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
    }
    
    /* Headers */
    h1 {
        color: #1e3d59;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    /* Cards */
    .stCard {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: white;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #17a2b8;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #138496;
        transform: translateY(-2px);
    }
    
    /* Text areas */
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        padding: 10px;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #17a2b8;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    with st.spinner('Extracting text from PDF...'):
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an expert resume analyzer. Please analyze this resume against the job description provided.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Provide a detailed analysis including:
    1. Key strengths and skills that match the job requirements (be specific)
    2. Missing skills or areas where the candidate needs improvement
    3. Concrete suggestions to improve the resume
    4. A percentage match score between the resume and job requirements
    5. Overall assessment of the candidate's fit for the role
    Format your response in clear sections with detailed explanations.
    """
    
    try:
        with st.spinner('AI is analyzing your resume...'):
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume analyzer who provides detailed, actionable feedback."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-guard-3-8b",  # Using Groq's most capable model
                temperature=0.7,
                max_tokens=4096
            )
        
        if completion and completion.choices:
            return completion.choices[0].message.content
        else:
            st.error("No response received from the AI model")
            return None
    except Exception as e:
        st.error(f"Error in AI analysis: {str(e)}")
        return None

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: black;
        color: #FFD700;
    }
    .main {
        padding: 2rem;
        background-color: black;
    }
    .stButton>button {
        width: 100%;
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }
    .st-emotion-cache-uf99v8 {
        background-color: black;
        color: #FFD700;
    }
    .st-emotion-cache-16idsys {
        color: #FFD700;
    }
    .st-emotion-cache-183lzff {
        color: #FFD700;
    }
    .streamlit-expanderHeader {
        color: #FFD700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header section with icon
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942799.png", width=80)
with col2:
    st.title("Resume Analysis Tool")
    st.markdown("*Let AI help you perfect your resume for your dream job* 🚀")

# Create two columns for inputs
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader("", type="pdf", help="Please upload a PDF file")
    if uploaded_file:
        st.success("Resume uploaded successfully!")

with right_col:
    st.markdown("### 💼 Job Description")
    job_description = st.text_area("", height=200, placeholder="Paste the job description here...")

# Center the analyze button
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    analyze_button = st.button("🔍 Analyze Resume", use_container_width=True)

if analyze_button:
    if uploaded_file is not None and job_description:
        try:
            # Extract text from resume
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Get analysis
            analysis = analyze_resume(resume_text, job_description)
            
            if analysis:
                # Display results in an expander
                st.markdown("### 📊 Analysis Results")
                
                # Split analysis into sections and display with formatting
                sections = analysis.split('\n\n')
                for section in sections:
                    if section.strip():
                        # Extract the section title (first line) and content (remaining lines)
                        lines = section.split('\n')
                        title = lines[0]
                        content = '\n'.join(lines[1:]) if len(lines) > 1 else ''
                        
                        with st.expander(title, expanded=True):
                            st.markdown(content)
            else:
                st.error("Failed to generate analysis. Please try again.")
            
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.error("Full error details:", exc_info=True)
    else:
        st.warning("⚠️ Please upload a resume and enter a job description to proceed")
