import pdfplumber
import docx2txt
import os
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import gdown
import zipfile

# -------------------------
# Download fine-tuned model from Google Drive
# -------------------------
def download_model():
    url = "https://drive.google.com/uc?id=1Zd7ApQCrOgH7MjwFDRFYEu9EO2Bmqmv1"
    output_zip = "fine_tuned_model.zip"
    
    if not os.path.exists("fine_tuned_model"):
        print("[INFO] Downloading fine-tuned model...")
        gdown.download(url, output_zip, quiet=False)
        with zipfile.ZipFile(output_zip, 'r') as zip_ref:
            zip_ref.extractall("fine_tuned_model")
        print("[INFO] Model downloaded and extracted successfully.")
    else:
        print("[INFO] Model already exists. Skipping download.")

# -------------------------
# Initialize the model
# -------------------------
download_model()
model = SentenceTransformer("fine_tuned_model")

# -------------------------
# Extract text from PDF or DOCX
# -------------------------
def extract_text(file):
    try:
        if hasattr(file, "name"):
            filename = file.name
        else:
            filename = file

        if filename.lower().endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            return text.strip()
        
        elif filename.lower().endswith('.docx'):
            return docx2txt.process(file).strip()
        
        else:
            print(f"[WARNING] Unsupported file type: {filename}")
            return ""
    except Exception as e:
        print(f"[ERROR] Failed to extract text: {e}")
        return ""

# -------------------------
# Hard keyword match
# -------------------------
def hard_match(resume_text, jd_keywords):
    matches = sum(1 for kw in jd_keywords if kw.lower() in resume_text.lower())
    return matches / max(1, len(jd_keywords))

# -------------------------
# Semantic similarity
# -------------------------
def semantic_score(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(score)

# -------------------------
# Weighted final score
# -------------------------
def calculate_score(resume_text, jd_keywords, jd_text):
    hard = hard_match(resume_text, jd_keywords)
    soft = semantic_score(resume_text, jd_text)
    final = 0.5 * hard + 0.5 * soft
    return round(final * 100, 2)

# -------------------------
# Generate verdict based on score
# -------------------------
def generate_verdict(score):
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"
