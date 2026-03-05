import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# ---------------------------
# 1️⃣ Load Dataset
# ---------------------------
df = pd.read_csv("case_files_total.csv")  # your dataset

# Keep required columns
data = df[["judgement", "label"]].dropna()

# Clean labels
data["label"] = data["label"].str.lower().str.strip()
data = data[data["label"] != "other"]

# Convert judgement to string
data["judgement"] = data["judgement"].astype(str)

# ---------------------------
# 2️⃣ Synthetic Case Duration
# ---------------------------
def estimate_duration(text):
    words = len(text.split())
    if words < 100:
        return 6
    elif words < 300:
        return 12
    elif words < 600:
        return 18
    else:
        return 24

data["case_duration"] = data["judgement"].apply(estimate_duration)

# ---------------------------
# 3️⃣ Features & Target
# ---------------------------
X = data["judgement"]
y_label = data["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_label, test_size=0.2, random_state=2, stratify=y_label
)

# ---------------------------
# 4️⃣ Build ML Pipeline
# ---------------------------
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=20000,
        stop_words="english",
        ngram_range=(1,2),
        min_df=2,
        max_df=0.9,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# ---------------------------
# 5️⃣ Train Model
# ---------------------------
print("Training Judgment Prediction Model...")
model.fit(X_train, y_train)

# ---------------------------
# 6️⃣ Training Accuracy
# ---------------------------
y_train_pred = model.predict(X_train)
train_acc = accuracy_score(y_train, y_train_pred)
print(f"Training Accuracy: {train_acc:.4f}")

# ---------------------------
# 7️⃣ Test Accuracy
# ---------------------------
y_test_pred = model.predict(X_test)
test_acc = accuracy_score(y_test, y_test_pred)
print(f"Test Accuracy: {test_acc:.4f}")

# Classification report
print("\nClassification Report (Test Set):")
print(classification_report(y_test, y_test_pred))

# ---------------------------
# 8️⃣ Save Model
# ---------------------------
with open("legal_case_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as legal_case_model.pkl")

# ---------------------------
# 9️⃣ Sample Prediction
# ---------------------------
sample_text = "The appeal filed by the petitioner for murder case is rejected by court."  # change text to test

# Predict Label
pred = model.predict([sample_text])[0]

# Confidence
prob = model.predict_proba([sample_text])[0]
confidence = float(prob.max()) * 100

# Case Category
def get_case_category(text):
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

category = get_case_category(sample_text)

# Case Duration (only if Accepted)
if pred.lower() == "accepted":
    duration_months = estimate_duration(sample_text)
    years = duration_months // 12
    rem = duration_months % 12
    if years > 0 and rem > 0:
        duration = f"{years} year(s) {rem} month(s)"
    elif years > 0:
        duration = f"{years} year(s)"
    else:
        duration = f"{rem} month(s)"
else:
    duration = "N/A"

# ---------------------------
# 10️⃣ Print Sample Output
# ---------------------------
print("\n===== Sample Prediction =====")
print(f"Label             : {pred.capitalize()}")
print(f"Case Category     : {category}")
print(f"Case Duration     : {duration}")
print(f"Confidence Score  : {confidence:.2f}%")