import streamlit as st
from utils import extract_text, calculate_score, generate_verdict, download_model
import pandas as pd
import os

st.title("Automated Resume Relevance Checker")

# -------------------------
# Student Dashboard
# -------------------------
st.header("Student Resume Submission")
uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description Here")

if uploaded_file and jd_text:
    resume_text = extract_text(uploaded_file)
    
    # Example: extracting keywords from JD (simplified)
    jd_keywords = jd_text.split()[:20]  # take first 20 words as dummy keywords
    
    score = calculate_score(resume_text, jd_keywords, jd_text)
    verdict = generate_verdict(score)
    
    st.write(f"**Relevance Score:** {score}")
    st.write(f"**Verdict:** {verdict}")

# -------------------------
# HR Dashboard
# -------------------------
st.header("HR Dashboard")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username == "hr" and password == "hr123":
    st.success("Logged in as HR")
    if os.path.exists("submissions.csv"):
        df = pd.read_csv("submissions.csv")
        st.dataframe(df)
    else:
        st.write("No submissions yet.")
    
    # Save submissions
    if uploaded_file and jd_text:
        new_data = {"Resume": uploaded_file.name, "Score": score, "Verdict": verdict}
        if os.path.exists("submissions.csv"):
            df = pd.read_csv("submissions.csv")
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        else:
            df = pd.DataFrame([new_data])
        df.to_csv("submissions.csv", index=False)
