import streamlit as st
import pandas as pd
import sqlite3
from utils import extract_text, hard_match, semantic_score, final_score, missing_skills

# Initialize SQLite DB
conn = sqlite3.connect('resume_checker.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS evaluations (
    resume_name TEXT,
    job_title TEXT,
    hard_score REAL,
    soft_score REAL,
    final_score REAL,
    verdict TEXT,
    missing_skills TEXT
)
''')
conn.commit()

st.title("Automated Resume Relevance Checker")

# ---------------- Student Dashboard ----------------
st.header("Student Dashboard")
resume_file = st.file_uploader("Upload Resume", type=["pdf","docx"])
jd_text = st.text_area("Paste Job Description here")

# Example JD skills (can parse from JD text in future)
jd_skills = ["Python","ML","NLP","Pandas","Tableau","Excel"]

if resume_file and jd_text:
    resume_text = extract_text(resume_file)
    hard = hard_match(resume_text, jd_skills)
    soft = semantic_score(resume_text, jd_text)
    score, verdict = final_score(hard, soft)
    missing = missing_skills(resume_text, jd_skills)

    # Display result immediately to student
    st.subheader("Evaluation Result")
    st.write(f"**Score:** {score:.2f}")
    st.write(f"**Verdict:** {verdict}")
    st.write(f"**Missing Skills:** {', '.join(missing)}")

    # Store in DB
    c.execute('''
        INSERT INTO evaluations (resume_name, job_title, hard_score, soft_score, final_score, verdict, missing_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (resume_file.name, "JD1", hard, soft, score, verdict, ", ".join(missing)))
    conn.commit()

# ---------------- HR Dashboard ----------------
st.header("HR Dashboard (Login)")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username=="hr" and password=="hackathon":
    st.subheader("All Evaluated Resumes")
    df = pd.read_sql_query("SELECT * FROM evaluations", conn)
    st.dataframe(df)
