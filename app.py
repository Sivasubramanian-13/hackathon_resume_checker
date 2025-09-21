import streamlit as st
from utils import extract_text, calculate_score, generate_verdict, save_submission, load_submissions

st.title("Automated Resume Relevance Check System")

# --- Student Section ---
st.header("Student Resume Submission")
with st.form("resume_form"):
    name = st.text_input("Enter Your Name")
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Paste Job Description")
    submitted = st.form_submit_button("Submit Resume")

    if submitted:
        if name and resume_file and jd_text:
            resume_text = extract_text(resume_file)
            score = calculate_score(resume_text, jd_text)
            verdict = generate_verdict(score)
            save_submission(name, score, verdict)
            st.success(f"Score: {score} | Verdict: {verdict}")
        else:
            st.error("Please fill all fields and upload resume.")

# --- HR Section ---
st.header("HR Dashboard")
hr_password = st.text_input("Enter HR Password", type="password")
if hr_password == "hr123":  # simple credential for demo
    st.subheader("All Submissions")
    df = load_submissions()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No submissions yet.")
