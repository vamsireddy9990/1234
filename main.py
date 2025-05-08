import streamlit as st
import PyPDF2
import io
from groq import Groq

# Set up Groq client
client = Groq(
    api_key= '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'
)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, job_description):
    prompt = f"""
    Analyze the following resume against the job description:
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Please provide:
    1. Key strengths matching the job requirements
    2. Areas of improvement or missing skills
    3. Specific suggestions to improve the resume
    4. Overall match percentage and likelihood of selection
    """
    
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-guard-3-8b",
        temperature=0.5,
    )
    
    return completion.choices[0].message.content

# Streamlit UI
# Set page configuration
st.set_page_config(page_title="Resume Analysis Tool", layout="wide")

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
            
            # Show processing message
            with st.spinner("🤖 AI is analyzing your resume..."):
                # Get analysis
                analysis = analyze_resume(resume_text, job_description)
                
                # Display results in an expander
                st.markdown("### 📊 Analysis Results")
                
                # Split analysis into sections and display with formatting
                sections = analysis.split('\n\n')
                for section in sections:
                    if section.strip():
                        with st.expander(section.split('\n')[0], expanded=True):
                            st.markdown(section)
                
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please upload a resume and enter a job description to proceed")
