import pdfplumber
import docx2txt
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import gdown
import zipfile

# Download and extract fine-tuned model from Google Drive
def download_model():
    url = "https://drive.google.com/uc?id=1Zd7ApQCrOgH7MjwFDRFYEu9EO2Bmqmv1"  # zip file ID
    output = "fine_tuned_model.zip"
    if not os.path.exists("fine_tuned_model"):
        gdown.download(url, output, quiet=False)
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall("fine_tuned_model")
        os.remove(output)
    print("Model ready.")

# Load model
download_model()
model = SentenceTransformer("fine_tuned_model")

# Extract text from PDF or DOCX
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    else:
        text = ""
    return text

# Calculate semantic similarity score
def calculate_score(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(score * 100, 2)

# Generate verdict
def generate_verdict(score):
    if score > 75:
        return "High"
    elif score > 50:
        return "Medium"
    else:
        return "Low"

# Save submission
def save_submission(name, score, verdict):
    data = {"Name": [name], "Score": [score], "Verdict": [verdict]}
    df = pd.DataFrame(data)
    if os.path.exists("submissions.csv"):
        df_existing = pd.read_csv("submissions.csv")
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv("submissions.csv", index=False)

# Load all submissions (for HR)
def load_submissions():
    if os.path.exists("submissions.csv"):
        return pd.read_csv("submissions.csv")
    return pd.DataFrame()
