from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
with open("legal_case_model.pkl", "rb") as f:
    model = pickle.load(f)


class CaseInput(BaseModel):
    text: str


# Helper: Case category detection
def get_case_category(text: str) -> str:
    text = text.lower()
    if "murder" in text or "theft" in text or "crime" in text or "police" in text:
        return "Criminal"
    elif "divorce" in text or "marriage" in text or "family" in text:
        return "Family"
    elif "property" in text or "land" in text or "ownership" in text:
        return "Property"
    elif "company" in text or "business" in text or "corporate" in text:
        return "Corporate"
    elif "contract" in text or "agreement" in text:
        return "Civil"
    else:
        return "General"


# Helper: Case duration estimation
def estimate_duration(text: str) -> str:
    words = len(text.split())
    if words < 100:
        months = 6
    elif words < 300:
        months = 12
    elif words < 600:
        months = 18
    else:
        months = 24
    years = months // 12
    rem = months % 12
    if years > 0 and rem > 0:
        return f"{years} year(s) {rem} month(s)"
    elif years > 0:
        return f"{years} year(s)"
    else:
        return f"{rem} month(s)"


@app.get("/")
def home():
    return {"message": "Legal Prediction API Running"}


@app.post("/predict")
def predict(data: CaseInput):
    text = data.text

    # 1️⃣ Predict label
    pred = model.predict([text])[0]
    prob = model.predict_proba([text])[0]
    confidence = float(np.max(prob)) * 100

    label = "Accepted" if pred.lower() == "accepted" else "Rejected"

    # 2️⃣ Case category
    case_category = get_case_category(text)

    # 3️⃣ Case duration only if Accepted
    case_duration = estimate_duration(text) if label == "Accepted" else "N/A"

    return {
        "label": label,
        "case_category": case_category,
        "case_duration": case_duration,
        "confidence_score": round(confidence, 2)
    }