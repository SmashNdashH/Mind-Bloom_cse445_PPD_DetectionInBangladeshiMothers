# Mind-Bloom_cse445_PPD_DetectionInBangladeshiMothers
Machine Learning for Prediction and Analysis of Postpartum Depression in Bangladeshi Mothers
11/27/2025- (IMPROVEMENTS) made a copy of the existing notebook for EDITS and IMPROVEMENTS.

Mind Bloom — PPD Detection in Bangladeshi Mothers
CSE445 Machine Learning Project (PPD Detection Using ML & Streamlit)
- A Mental-Health Screening Tool for Postpartum Mothers
- Overview

Mind Bloom is a machine-learning powered application designed to detect Postpartum Depression (PPD) in Bangladeshi mothers using demographic, clinical, and psychosocial features.
The project uses Multiple ML algorithms and a real-world inspired dataset to classify the EPDS Result (High, Medium, Low) using supervised learning.

The goal is to support early detection, awareness, and further clinical screening.

The system includes:

✔ Data preprocessing & exploratory analysis

✔ Model training, comparison, & evaluation

✔ Saving the trained ML model (.pkl files)

✔ A frontend web application using Streamlit

✔ Two input modes: CSV upload mode + Manual single-patient mode

✔ User-friendly prediction interface

🚀 Features
🧩 1. Machine Learning Model

Models tested:

Logistic Regression

Random Forest (Best Model)

KNN

Decision Tree

SVM

Metrics evaluated: Accuracy, Precision, Recall, F1-Score

The Random Forest model achieved the best performance.

🧠 2. Frontend Web App using Streamlit

The application provides two modes:

📁 CSV Upload Mode (Batch Prediction)

Upload a CSV file containing multiple patient records →
Model predicts EPDS Result for all patients at once.

✍️ Manual Input Mode (Single Patient Prediction)

Fill a form with features (Age, Score, etc.) →
Receive one PPD prediction instantly.

🔄 3. Output

Predictions returned as: High / Medium / Low

Downloadable results as CSV

Real-time preprocessing applied (scaling, one-hot encoding)

🗂️ Repository Structure
Mind-Bloom_cse445_PPD_DetectionInBangladeshiMothers/

│
├── app.py                     # Streamlit frontend
├── VERSION_Abrar_Grp_Assign.ipynb   # ML notebook (EDA + modeling)
├── PPD_dataset_v2.csv         # Dataset used for training/testing
│
├── best_model.pkl             # Final Random Forest model
├── ohe_final.pkl              # One-Hot Encoder object
├── scaler.pkl                 # StandardScaler object
├── final_numeric.pkl          # List of numeric columns
├── final_cat_cols.pkl         # List of categorical columns
├── label_encoder.pkl          # LabelEncoder for EPDS Result
│
├── README.md                  # Project documentation
└── .gitignore                 # Virtual env & cache ignored


⚙️ How to Run the Project Locally
1️⃣ Clone the Repository
git clone https://github.com/SmashNdashH/Mind-Bloom_cse445_PPD_DetectionInBangladeshiMothers
cd Mind-Bloom_cse445_PPD_DetectionInBangladeshiMothers

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt  (optional if available)


Or manually:

pip install pandas scikit-learn streamlit joblib numpy matplotlib seaborn

4️⃣ Run the Streamlit App
streamlit run app.py

5️⃣ Open in Browser

The app will open automatically, or visit:

http://localhost:8501

📊 Dataset Description

The dataset includes features related to:

Demographics (Age, Residence, Education)

Psychosocial factors

EPDS & PHQ9 scores

Pregnancy & maternal history

Social and emotional support indicators

Target variable:

EPDS Result → High / Medium / Low

💡 Results Summary

Best Model: Random Forest

Key Advantage: High F1-Score across classes

Handles both numeric and categorical data efficiently

Robust after preprocessing (scaling, encoding)

🌐 Future Improvements

Add SHAP explainability (why the model predicts High/Low)

Deploy online using Streamlit Cloud / HuggingFace Spaces

Add sentiment analysis on free-text symptoms

Improve dataset with longitudinal postpartum follow-ups
