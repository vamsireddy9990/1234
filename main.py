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
        model="llama3-70b-8192",
        temperature=0.5,
    )
    
    return completion.choices[0].message.content

# Streamlit UI
st.title("Resume Analysis Tool")
st.write("Upload your resume and enter the job description to get personalized feedback")

# File upload for resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

# Text area for job description
job_description = st.text_area("Enter the Job Description", height=200)

if st.button("Analyze"):
    if uploaded_file is not None and job_description:
        try:
            # Extract text from resume
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Show processing message
            with st.spinner("Analyzing your resume..."):
                # Get analysis
                analysis = analyze_resume(resume_text, job_description)
                
                # Display results
                st.subheader("Analysis Results")
                st.write(analysis)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload a resume and enter a job description")
