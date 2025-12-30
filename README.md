# 📌 Day 03 — Customer Churn Prediction Pipeline  

This project implements a full end-to-end ML pipeline for predicting customer churn using a KNN model, FastAPI backend, and Streamlit dashboard with saved prediction history.

## 🧠 Project Workflow
Jupyter Notebook → Model (.pkl) → FastAPI API → Streamlit Dashboard → Local Prediction History  

## 🗂 Folder Structure  
Day03_KNN_CustomerChurnPipeline/  
├── notebooks/  
│   └── Day03_KNN.ipynb  
├── model/  
│   └── churn_knn_pipeline.pkl  
├── api/  
│   └── app.py  
├── dashboard/  
│   └── app.py  
├── data/  
│   └── predictions.csv  
└── README.md  

## ⚙️ Setup  
python -m venv venv  
venv\Scripts\activate  
pip install fastapi uvicorn streamlit scikit-learn pandas numpy seaborn matplotlib joblib  

## 🚀 Run
uvicorn api.app:app --reload  
streamlit run dashboard/app.py  

## 🛰 API Example  
POST http://127.0.0.1:8000/predict  
{  
  "gender": 1,  
  "SeniorCitizen": 0,  
  "Partner": 1,  
  "Dependents": 0,  
  "tenure": 16,  
  "PhoneService": 1,  
  "MultipleLines": 0,  
  "InternetService": 2,  
  "OnlineSecurity": 1,  
  "OnlineBackup": 0,  
  "DeviceProtection": 1,  
  "TechSupport": 0,  
  "StreamingTV": 2,  
  "StreamingMovies": 1,  
  "Contract": 1,  
  "PaperlessBilling": 1,  
  "PaymentMethod": 2,  
  "MonthlyCharges": 71.25,  
  "TotalCharges": 890.0  
}  

## 📊 Dashboard Features

✔ **Human-friendly inputs** (no 0/1 confusion)  
✔ **Prediction stored automatically** in `predictions.csv`  
✔ **Analytics generated from saved predictions**  
✔ **Delete single, multiple, or all logs**

---

## 📈 Current Graphs

- **Churn Count Summary**
- **Tenure Impact vs Churn**
- **Charge-based churn indicators**

---

## 🛠 Future Enhancements

- Add **churn probability score / risk meter**
- Add **PDF/CSV downloadable reports**
- **Docker containerization** for deployment
- Deploy **API on Render / Railway**
- Deploy **dashboard to Streamlit Cloud**

---

