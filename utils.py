import pdfplumber
import docx2txt
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load fine-tuned model once
model = SentenceTransformer("fine_tuned_model")

def extract_text(file):
    """
    Accepts either a file path (str) or Streamlit UploadedFile object
    """
    # If Streamlit UploadedFile, get the buffer
    if hasattr(file, "read"):
        if file.name.endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                return "\n".join([page.extract_text() for page in pdf.pages])
        elif file.name.endswith('.docx'):
            return docx2txt.process(file)
        else:
            return ""
    else:  # Regular file path as string
        if file.endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                return "\n".join([page.extract_text() for page in pdf.pages])
        elif file.endswith('.docx'):
            return docx2txt.process(file)
        else:
            return ""

# Hard match score
def hard_match(resume_text, jd_skills):
    count = 0
    for skill in jd_skills:
        for word in resume_text.split():
            if fuzz.ratio(skill.lower(), word.lower()) > 80:
                count += 1
                break
    return (count / len(jd_skills)) * 100

# Semantic similarity score
def semantic_score(resume_text, jd_text):
    res_emb = model.encode(resume_text)
    jd_emb = model.encode(jd_text)
    return cosine_similarity([res_emb], [jd_emb])[0][0] * 100

# Final score & verdict
def final_score(hard, soft):
    score = 0.6*hard + 0.4*soft
    if score >= 75: verdict = "High"
    elif score >= 50: verdict = "Medium"
    else: verdict = "Low"
    return score, verdict

# Missing skills
def missing_skills(resume_text, jd_skills):
    return [skill for skill in jd_skills if skill.lower() not in resume_text.lower()]
