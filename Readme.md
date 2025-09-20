# Automated Resume Relevance Checker

## Overview

This project provides an automated solution for evaluating resumes against job descriptions. It offers two main interfaces:

- **Student Dashboard**: Allows students to upload their resumes and receive an evaluation score, verdict, and a list of missing skills.
- **HR Dashboard**: Enables HR personnel to log in and view all previous resume evaluations.

## Features

- **Resume Evaluation**: Analyzes resumes based on hard skill matches and semantic similarity to the job description.
- **Verdict Classification**: Categorizes resumes into 'High', 'Medium', or 'Low' relevance.
- **Missing Skills Detection**: Identifies skills present in the job description but absent in the resume.
- **HR Dashboard**: Provides a secure login for HR to access all evaluations.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.12.5
- **Libraries**: 
  - `pdfplumber`, `docx2txt` for resume parsing
  - `fuzzywuzzy` for hard skill matching
  - `sentence-transformers` for semantic analysis
  - `scikit-learn` for cosine similarity
  - `sqlite3` for database management

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Sivasubramanian-13/hackathon_resume_checker.git
cd hackathon_resume_checker
