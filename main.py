from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib

# ---------------------------
# Load model
# ---------------------------
model = joblib.load("best_model.pkl")


# ---------------------------
# Normalize helper
# ---------------------------
def norm(x):
    if x is None:
        return "nan"
    x = str(x).strip().lower()
    if x in ["", "none", "nan"]:
        return "nan"
    return x


# ---------------------------
# Emotional scoring helpers
# ---------------------------

FEELING_MAP = {
    "happy": 0,
    "good": 0,
    "neutral": 1,
    "sad": 2,
    "bad": 2,
    "worried": 2,
    "tired": 2,
    "afraid": 3,
}

SUPPORT_MAP = {
    "high": 0,
    "medium": 1,
    "low": 2,
}

YESNO_MAP = {
    "no": 0,
    "yes": 2,
}

def score_feeling(value):
    return FEELING_MAP.get(norm(value), 1)

def score_support(value):
    return SUPPORT_MAP.get(norm(value), 1)

def score_yesno(value):
    return YESNO_MAP.get(norm(value), 0)


# ---------------------------
# Input Schema (PHQ9 removed)
# ---------------------------
class Input(BaseModel):
    Age: float
    Number_of_the_latest_pregnancy: float

    Education_Level: str
    Husbands_education_level: str
    Total_children: str
    Disease_before_pregnancy: str
    Family_type: str

    Feeling_about_motherhood: str
    Recieved_Support: str
    Need_for_Support: str
    Major_changes_or_losses: str
    Abuse: str
    Trust_and_share_feelings: str
    Feeling_for_regular_activities: str
    Angry_after_latest_child_birth: str

    Pregnancy_length: str
    Pregnancy_plan: str
    Regular_checkups: str
    Fear_of_pregnancy: str
    Diseases_during_pregnancy: str

    Relationship_with_inlaws: str
    Relationship_with_husband: str
    Relationship_with_newborn: str
    Relationship_between_father_and_newborn: str
    Age_of_immediate_older_children: str
    Birth_compliancy: str
    Breastfeed: str
    Worry_about_newborn: str
    Relax_sleep_when_tended: str
    Relax_sleep_when_asleep: str

    Depression_before_pregnancy: str
    Depression_during_pregnancy: str
    Newborn_illness: str
    PHQ9_Result: str | None = None  # ignored from user


# ---------------------------
# Build cat_maps (same as before)
# ---------------------------
# KEEP your existing cat_maps and field_map here
# (Do NOT delete them)

# Mapping of JSON keys to original column names
field_map = {
    "Education_Level": "Education_Level",
    "Husbands_education_level": "Husbands_education_level",
    "Total_children": "Total_children",
    "Disease_before_pregnancy": "Disease_before_pregnancy",
    "Family_type": "Family_type",
    "Feeling_about_motherhood": "Feeling_about_motherhood",
    "Recieved_Support": "Recieved_Support",
    "Need_for_Support": "Need_for_Support",
    "Major_changes_or_losses": "Major_changes_or_losses",
    "Abuse": "Abuse",
    "Trust_and_share_feelings": "Trust_and_share_feelings",
    "Feeling_for_regular_activities": "Feeling_for_regular_activities",
    "Angry_after_latest_child_birth": "Angry_after_latest_child_birth",
    "Pregnancy_length": "Pregnancy_length",
    "Pregnancy_plan": "Pregnancy_plan",
    "Regular_checkups": "Regular_checkups",
    "Fear_of_pregnancy": "Fear_of_pregnancy",
    "Diseases_during_pregnancy": "Diseases_during_pregnancy",
    "Relationship_with_inlaws": "Relationship_with_inlaws",
    "Relationship_with_husband": "Relationship_with_husband",
    "Relationship_with_newborn": "Relationship_with_newborn",
    "Relationship_between_father_and_newborn": "Relationship_between_father_and_newborn",
    "Age_of_immediate_older_children": "Age_of_immediate_older_children",
    "Birth_compliancy": "Birth_compliancy",
    "Breastfeed": "Breastfeed",
    "Worry_about_newborn": "Worry_about_newborn",
    "Relax_sleep_when_tended": "Relax_sleep_when_tended",
    "Relax_sleep_when_asleep": "Relax_sleep_when_asleep",
    "Depression_before_pregnancy": "Depression_before_pregnancy",
    "Depression_during_pregnancy": "Depression_during_pregnancy",
    "Newborn_illness": "Newborn_illness",
}

# Categorical feature encoding maps
cat_maps = {
    "Education_Level": {"nan": 0},
    "Husbands_education_level": {"nan": 0},
    "Total_children": {"nan": 0},
    "Disease_before_pregnancy": {"nan": 0, "no": 0, "yes": 1},
    "Family_type": {"nan": 0},
    "Feeling_about_motherhood": {"nan": 1},
    "Recieved_Support": {"nan": 1},
    "Need_for_Support": {"nan": 1},
    "Major_changes_or_losses": {"nan": 0, "no": 0, "yes": 1},
    "Abuse": {"nan": 0, "no": 0, "yes": 1},
    "Trust_and_share_feelings": {"nan": 0, "no": 0, "yes": 1},
    "Feeling_for_regular_activities": {"nan": 1},
    "Angry_after_latest_child_birth": {"nan": 1},
    "Pregnancy_length": {"nan": 0},
    "Pregnancy_plan": {"nan": 0, "planned": 0, "unplanned": 1},
    "Regular_checkups": {"nan": 0, "no": 0, "yes": 1},
    "Fear_of_pregnancy": {"nan": 1},
    "Diseases_during_pregnancy": {"nan": 0, "no": 0, "yes": 1},
    "Relationship_with_inlaws": {"nan": 0},
    "Relationship_with_husband": {"nan": 0},
    "Relationship_with_newborn": {"nan": 0},
    "Relationship_between_father_and_newborn": {"nan": 0},
    "Age_of_immediate_older_children": {"nan": 0},
    "Birth_compliancy": {"nan": 0, "yes": 0, "no": 1},
    "Breastfeed": {"nan": 0, "yes": 0, "no": 1},
    "Worry_about_newborn": {"nan": 1},
    "Relax_sleep_when_tended": {"nan": 1},
    "Relax_sleep_when_asleep": {"nan": 1},
    "Depression_before_pregnancy": {"nan": 0, "no": 0, "yes": 1},
    "Depression_during_pregnancy": {"nan": 0, "no": 0, "yes": 1},
    "Newborn_illness": {"nan": 0, "no": 0, "yes": 1},
}


# ---------------------------
# Compute PHQ9 & EPDS from answers
# ---------------------------
def compute_scores(d):
    emotional = (
        score_feeling(d["Feeling_about_motherhood"]) +
        score_feeling(d["Feeling_for_regular_activities"]) +
        score_feeling(d["Angry_after_latest_child_birth"])
    )

    support = (
        score_support(d["Recieved_Support"]) +
        score_support(d["Need_for_Support"])
    )

    stress = (
        score_yesno(d["Major_changes_or_losses"]) +
        score_yesno(d["Abuse"]) +
        score_yesno(d["Trust_and_share_feelings"])
    )

    PHQ9 = emotional + support
    EPDS = PHQ9 + stress * 0.5

    # Determine PHQ9 category
    if PHQ9 <= 4:
        result = "Minimal"
    elif PHQ9 <= 9:
        result = "Mild"
    elif PHQ9 <= 14:
        result = "Moderate"
    elif PHQ9 <= 19:
        result = "Moderately Severe"
    else:
        result = "Severe"

    return PHQ9, EPDS, result


# ---------------------------
# FastAPI init
# ---------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# Predict Endpoint
# ---------------------------
@app.post("/predict")
def predict(data: Input):
    d = data.dict()

    # Compute internal scores
    PHQ9_Score, EPDS_Score, PHQ9_Result = compute_scores(d)

    # Numerical features
    Age = d["Age"]
    Preg = d["Number_of_the_latest_pregnancy"]

    Age_EPDS = Age * EPDS_Score
    Preg_EPDS = Preg * EPDS_Score

    vector = [Age, Preg, PHQ9_Score, Age_EPDS, Preg_EPDS]

    # Categorical
    for json_key, original_col in field_map.items():
        raw = norm(d[json_key])
        encoded_val = cat_maps[original_col].get(raw, cat_maps[original_col]["nan"])
        vector.append(encoded_val)

    X = np.array(vector).reshape(1, -1)

    pred = model.predict(X)[0]

    # Probabilities
    proba = {}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        for cls, p in zip(model.classes_, probs):
            proba[str(cls)] = float(p)

    return {
        "prediction": str(pred),
        "PHQ9_Score": PHQ9_Score,
        "EPDS_Score": EPDS_Score,
        "PHQ9_Result": PHQ9_Result,
        "probabilities": proba
    }
