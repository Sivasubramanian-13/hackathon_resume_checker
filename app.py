import streamlit as st
from utils import extract_text, calculate_score, generate_verdict
import pandas as pd
import os

st.title("Automated Resume Relevance Checker")

# -------------------------
# Upload JD
# -------------------------
st.header("Upload Job Description")
jd_file = st.file_uploader("Upload JD (.txt or .pdf)", type=["txt", "pdf", "docx"])
jd_text = ""
jd_keywords = []

if jd_file:
    jd_text = extract_text(jd_file)
    jd_keywords = jd_text.split()  # simple keyword extraction, can be improved

# -------------------------
# Upload Resume
# -------------------------
st.header("Upload Your Resume")
resume_file = st.file_uploader("Upload Resume (.pdf/.docx)", type=["pdf", "docx"])

if resume_file and jd_text:
    resume_text = extract_text(resume_file)
    score = calculate_score(resume_text, jd_keywords, jd_text)
    verdict = generate_verdict(score)
    
    st.subheader("Result")
    st.write(f"**Relevance Score:** {score}")
    st.write(f"**Verdict:** {verdict}")
